import gdown
import pandas as pd
import os
import json
import argparse
import sys

def load_jeopardy_data(
    url: str = 'https://drive.google.com/uc?id=0BwT5wj_P7BKXb2hfM3d2RHU1ckE',
    data_dir: str = None,
    filename: str = 'jeopardy_data.json'
) -> pd.DataFrame:
    """
    Download (if needed) and load the Jeopardy data as a pandas DataFrame.

    Args:
        url (str): Google Drive URL to download the data from.
        data_dir (str): Directory to store the data file. Defaults to ../data relative to this file.
        filename (str): Name of the JSON file.

    Returns:
        pd.DataFrame: The loaded Jeopardy data.
    """
    # Determine data directory
    if data_dir is None:
        SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        PARENT_DIR = os.path.dirname(SRC_DIR)
        data_dir = os.path.join(PARENT_DIR, 'data')
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
        with open(output, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("File read successfully as JSON.")
        print("Shape:", df.shape)
        print("Columns:", df.columns.tolist())
        print("\nPercentage of missing values per column:")
        print((df.isnull().mean() * 100).round(2))
        return df
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download (if needed) and load the Jeopardy data as a pandas DataFrame."
    )
    parser.add_argument('--url', type=str, default='https://drive.google.com/uc?id=0BwT5wj_P7BKXb2hfM3d2RHU1ckE',
                        help='Google Drive URL to download the data from.')
    parser.add_argument('--data_dir', type=str, default=None,
                        help='Directory to store the data file. Defaults to ../data relative to this file.')
    parser.add_argument('--filename', type=str, default='jeopardy_data.json',
                        help='Name of the JSON file.')

    args = parser.parse_args()

    try:
        df = load_jeopardy_data(
            url=args.url,
            data_dir=args.data_dir,
            filename=args.filename
        )
        print("\nFirst 5 rows of the data:")
        print(df.head())
    except Exception as e:
        print(f"Failed to load Jeopardy data: {e}", file=sys.stderr)
        sys.exit(1)
