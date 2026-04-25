import os
import logging
import ast
import argparse

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_raw_data(input_path="data/raw/patterns_raw.csv"):
    """
    This function loads the input raw input data

    Args:
        input_path: path to raw input csv file

    Returns:
        DataFrame: a DataFrame of patten details

    """
    pattern_details = pd.read_csv(input_path)
    logger.info("Loaded %d patterns", len(pattern_details))
    return pattern_details


def drop_sparse_columns(pattern_details, threshold=50):
    """
    This function drops columens that have missing values greater than a given threshhold

    Args:
        pattern_details: a dataframe of pattern details
        threshold: threshhold of tolerated missing value percentage

    Returns:
        Dataframe: pattern details dataframe after sparse columns are removed
    """
    missing_value_percentage = (
        pattern_details.isnull().sum() / len(pattern_details)
    ) * 100
    columns_to_drop = missing_value_percentage[
        missing_value_percentage > threshold
    ].index
    cleaned = pattern_details.drop(columns=columns_to_drop)
    logger.info(
        "Dropped %d columns with >%d%% missing values: %s",
        len(columns_to_drop),
        threshold,
        list(columns_to_drop),
    )
    return cleaned


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess raw Ravelry pattern data")
    parser.add_argument(
        "--input", default="data/raw/patterns_raw.csv", help="path to raw CSV"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=50,
        help="missing value percentage threshold for column dropping",
    )
    args = parser.parse_args()

    df = load_raw_data(args.input)
    df = drop_sparse_columns(df, threshold=args.threshold)
    logger.info("Final shape: %s", df.shape)
