import gdown
import pandas as pd
import os
import json

# File configuration
# Look for data in parent folder of src
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SRC_DIR)
data_dir = os.path.join(PARENT_DIR, 'data')
output = os.path.join(data_dir, 'jeopardy_data.json')
url = 'https://drive.google.com/uc?id=0BwT5wj_P7BKXb2hfM3d2RHU1ckE'

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

# Read the JSON file and show some stats
try:
    print("Reading JSON file...")
    with open(output, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    print("File read successfully as JSON.")

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # Show percentage of missing values per column
    print("\nPercentage of missing values per column:")
    print((df.isnull().mean() * 100).round(2))

except Exception as e:
    print(f"Error reading JSON file: {e}")
    df = None