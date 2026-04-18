"""
This module runs ravelry_client.py to collect data and stores it as csv
"""

import argparse
import os
import logging

import pandas as pd

from src.data.ravelry_client import RavelryClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def collect_patterns(pages=100):
    """
    This function collects ravelry patterns

    Args:
        pages (int): number of pages to collect

    Returns:
        list: list of patterns collected
    """
    patterns = []
    client = RavelryClient()
    logger.info("Starting data collection for %d pages", pages)

    for page in range(1, pages + 1):
        logger.info("Fetching data for page: %d", page)
        patterns.extend(client.search_patterns(page=page)["patterns"])

    logger.info("Collected %d patterns", len(patterns))
    return patterns


def save_patterns(patterns, output_path="data/raw/patterns_raw.csv"):
    """
    This functions saves a list of collected patterns as a csv file

    Args:
        patterns (list): list of dict patterns
        output_path (str): path where csv will be saved

    """
    # create the patterns directory
    directory = os.path.dirname(output_path)
    os.makedirs(directory, exist_ok=True)

    # convert list of pattern dict into datafarame
    patterns_dataframe = pd.DataFrame(patterns)

    # save patterns as csv
    patterns_dataframe.to_csv(output_path, index=False)

    logger.info("Data saved to %s", output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collect crochet patterns from Ravelry API"
    )
    parser.add_argument(
        "--pages", type=int, default=2, help="number of pages to collect"
    )
    args = parser.parse_args()
    patterns = collect_patterns(pages=args.pages)
    save_patterns(patterns)
