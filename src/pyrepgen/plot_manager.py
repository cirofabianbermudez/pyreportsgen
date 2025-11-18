import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import logging

def create_commit_plot(all_dates: list, all_counts: list, 
                       author: str, email: str
                       ) -> None:
    """
    Creates and shows a plot of commits over time.

    Args:
        all_dates (list): List of dates.
        all_counts (list): List of commit counts corresponding to the dates.
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set font settings
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "GitLab Sans"]

    # Plot data
    ax.plot(all_dates, all_counts,
        color="#7282ee", 
        linewidth=2,
        marker="o",
        markersize=6,
        label="Commits"
    )

    # Grid
    ax.grid(True, axis="y", linestyle="-", alpha=0.5)

    # Axis labels
    ax.fill_between(all_dates, all_counts, 0, alpha=0.3, color="#7282ee")
    ax.set_ylabel("Commits", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month", fontsize=16, fontweight="bold")
    
    # Axis ticks configuration
    ax.tick_params(axis="x", colors="#626168", labelsize=12)
    ax.tick_params(axis="y", colors="#626168", labelsize=12)


    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    # Set axis limits
    ax.set_ylim(0, max(all_counts) + 1)

    # Manual limits
    start = datetime(2024, 9, 15).date()
    end   = datetime(2024, 10, 17).date()
    ax.set_xlim(start, end)
    # Automatic
    # ax.set_xlim(all_dates[0], all_dates[-1])

    # Vertical lines and marker texts
    first_commit = datetime(2024, 9, 20).date()
    last_commit = datetime(2024, 10, 14).date()
    ax.axvline(first_commit, color="#7282ee", linewidth=2, alpha=0.5)
    ax.axvline(last_commit, color="#7282ee", linewidth=2, alpha=0.5)

    # First commits text
    label_height = max(all_counts) - 1
    ax.annotate(
            f"{first_commit.strftime("%b %#d, %Y")}",
            xy=(first_commit, label_height),
            xycoords="data",
            xytext=(8, 0),
            textcoords="offset points",
            fontsize=12,
            color="#333333",
            fontweight="bold",
            ha="left",
            va="bottom",
            )
    # ax.text(
    #     first_commit, 
    #     label_height,
    #     f"{first_commit.strftime("%b %#d, %Y")}",
    #     fontsize=12,
    #     color="#333333",
    #     fontweight="bold",
    #     ha="left",
    #     va="bottom",
    # )

    # Last commits text
    ax.text(
        last_commit,
        label_height,
        f"{last_commit.strftime("%b %#d, %Y")}",
        fontsize=12,
        color="#333333",
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    # Title
    ax.set_title(
        f"{author}\n",
        fontsize=16,
        fontweight="bold",
        loc="left"
    )

    # Total commits in the range
    total_commits = 0
    for d, count in zip(all_dates, all_counts):
        if first_commit <= d <= last_commit:
            total_commits += count
    
    logging.info("Generating commit plot")
    logging.info(f"xlim: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    logging.info(f"Total commits in range: {total_commits}")

    ax.text(
        0, 1.015,
        f"{total_commits} commits ({email})",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="normal",
        ha="left",
        va="bottom"
    )

    ax.legend()
    fig.tight_layout()
    plt.show()
