import logging
import argparse
from pathlib import Path

import os
import sys
import yaml
import json

from .gitlab_fetch import fetch_all_commits, filter_out_merge_commits, filter_commits_by_author_email, build_commit_histogram_by_date, fill_missing_days_in_histogram
from .plot_manager import create_commit_plot

def main() -> None:

    parser = argparse.ArgumentParser(
        prog="pyrepgen",
        description="Generate reports from GitLab/GitHub repositories for verification reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="TODO"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        metavar="FILE",
        help="YAML configuration file path"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        required=False,
        metavar="MODE",
        default="normal",
        choices=["normal", "read"],
        help="Operation mode (choices: normal, read) [default: normal]",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=False,
        metavar="FILE",
        help="Input JSON file path"
    )
    
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]: %(message)s",
    )
    logging.info("Starting report generation")
    
    # Mode selection logic
    mode = args.mode
    logging.info(f"MODE: {mode}")
    if mode == "read" and not args.input:
        logging.error("Input JSON file must be specified in read mode")
        sys.exit(1)
    
    # Load YAML config
    config_path = args.config
    if config_path.exists() is False:
        logging.error(f"Configuration file {config_path} does not exist")
        sys.exit(1)
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    
    gitlab_url   = data.get("gitlab_url", "")
    project_id   = data.get("project_id", "")
    ref_name     = data.get("ref_name", "main")
    output_json  = data.get("output_json", "commits.json")
    author_email = data.get("author_email", "")
    since        = data.get("since", None)
    until        = data.get("until", None)

    if not gitlab_url or not project_id or not author_email:
        logging.error("gitlab_url, project_id, and author_email must be specified in the config file")
        sys.exit(1)

    logging.info(f"YAML configuration loaded")
    logging.info(f"GitLab URL:   {gitlab_url}")
    logging.info(f"Project ID:   {project_id}")
    logging.info(f"Branch:       {ref_name}")
    logging.info(f"Output JSON:  {output_json}")
    logging.info(f"Author Email: {author_email}")
    logging.info(f"Since:        {since}")
    logging.info(f"Until:        {until}")
    
    # Fetch or read commits
    if args.mode == "read":
        # Read commits from input JSON file
        input_path = args.input
        logging.info(f"Reading commits from {input_path}")
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                all_commits = json.load(f)
        except FileNotFoundError:
            logging.error(f"Input file {input_path} not found")
            sys.exit(1)
    else:
        access_token = os.environ.get("GITLAB_TOKEN")
        if not access_token:
            logging.error("GITLAB_TOKEN environment variable not set")
            sys.exit(1)
        logging.info(f"GITLAB_TOKEN found in environment variables")

        logging.info("Getting information from GitLab API")
        all_commits = fetch_all_commits(
            gitlab_url=gitlab_url,
            project_id=project_id,
            access_token=access_token,
            ref_name=ref_name,
            output_json=output_json,
            since=since,
            until=until
        )

    # Filter commits
    filter_commits = filter_out_merge_commits(all_commits)
    logging.info(f"Removing merge commits")
    logging.info(f"Extracted: {len(filter_commits)} commits")

    filter_commits = filter_commits_by_author_email(filter_commits, author_email)
    logging.info(f"Filtering by author email")
    logging.info(f"Extracted: {len(filter_commits)} commits")
    
    histogram = build_commit_histogram_by_date(filter_commits)
    dates, counts = fill_missing_days_in_histogram(histogram)
    
    logging.info(f"First commit date: {dates[0].strftime('%Y-%m-%d')}")
    logging.info(f"Last commit date: {dates[-1].strftime('%Y-%m-%d')}")

    # Generate plot
    create_commit_plot(dates, counts, author="Ciro Fabian Bermudez Marquez", email=author_email)
    
if __name__ == "__main__":
    main()
