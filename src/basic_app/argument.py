"""Provide CLI input."""
import argparse

def parse_args() -> argparse.Namespace:
    """Parse arguments and return."""
    parser = argparse.ArgumentParser(
        description="Command line options for basic-app")

    parser.add_argument("--envfile",
                        type=str,
                        default=".env",
                        help="path to a envioronment variable file")

    return parser.parse_args()
