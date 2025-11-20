import argparse

class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=120)