#!/usr/bin/env python3
"""
Jeopardy Data Download and Exploratory Data Analysis

Downloads Jeopardy! data from Google Drive and performs basic EDA.
Handles automatic downloading, data loading, and missing value analysis.

Usage: python data_download_and_eda.py [--filename FILE] [--data_dir DIR]
"""

import gdown
import pandas as pd
import os
import json
import argparse
import sys
from typing import Optional


def load_jeopardy_data(
    url: str = "https://drive.google.com/uc?id=0BwT5wj_P7BKXb2hfM3d2RHU1ckE",
    data_dir: Optional[str] = None,
    filename: str = "jeopardy_data.json",
) -> pd.DataFrame:
    """
    Download (if needed) and load the Jeopardy data as a pandas DataFrame.

    Args:
        url (str): Google Drive URL to download from
        data_dir (Optional[str]): Directory to store data (default: ../data)
        filename (str): JSON filename (default: 'jeopardy_data.json')

    Returns:
        pd.DataFrame: Loaded Jeopardy data with basic EDA output
    """
    # Determine data directory - if not provided, use ../data relative to this file
    if data_dir is None:
        SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        PARENT_DIR = os.path.dirname(SRC_DIR)
        data_dir = os.path.join(PARENT_DIR, "data")

    output = os.path.join(data_dir, filename)

    # Ensure data directory exists
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist. Creating it...")
        os.makedirs(data_dir, exist_ok=True)

    # Download file if it doesn't exist
    if not os.path.exists(output):
        print(f"File not found at {output}. Downloading...")
        gdown.download(url, output, quiet=False)
    else:
        print(f"File already exists at {output}. Skipping download.")

    # Read the JSON file and return as DataFrame
    try:
        print("Reading JSON file...")
        with open(output, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("File read successfully as JSON.")

        # Basic exploratory data analysis
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nPercentage of missing values per column:")
        missing_percentages = (df.isnull().mean() * 100).round(2)
        print(missing_percentages)

        return df
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file {output}: {e}")
        raise
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        raise


if __name__ == "__main__":
    # Command-line interface
    parser = argparse.ArgumentParser(description="Download and load Jeopardy data")
    parser.add_argument(
        "--url",
        type=str,
        default="https://drive.google.com/uc?id=0BwT5wj_P7BKXb2hfM3d2RHU1ckE",
        help="Google Drive URL",
    )
    parser.add_argument(
        "--data_dir", type=str, default=None, help="Data directory (default: ../data)"
    )
    parser.add_argument(
        "--filename", type=str, default="jeopardy_data.json", help="JSON filename"
    )

    args = parser.parse_args()

    try:
        df = load_jeopardy_data(
            url=args.url, data_dir=args.data_dir, filename=args.filename
        )

        print("\nFirst 5 rows of the data:")
        print(df.head())
        print(f"\nData loaded! Total questions: {len(df)}")

    except Exception as e:
        print(f"Failed to load Jeopardy data: {e}", file=sys.stderr)
        sys.exit(1)
