#!/usr/bin/env python3
"""
Simple Jeopardy Dataset Curation for NER Validation

Creates three subsets:
1. Questions with numbers
2. Questions with non-English words
3. Questions with unusual proper nouns

This version only uses the 'question' field for all curation tasks,
as in data_download_and_eda.py.
"""

import sys
import json
import argparse
import random
from pathlib import Path
from datetime import datetime

import pandas as pd
from tqdm import tqdm

from data_download_and_eda import load_jeopardy_data
from check_for_numbers import contains_number
from check_for_non_english_words import contains_non_english_and_words
from check_for_unusual_proper_nouns import has_unusual_proper_nouns

def get_question_text(row):
    # Use only the 'question' field (case-insensitive)
    for key in ['question']:
        if key in row and pd.notna(row[key]):
            return str(row[key])
    return ""

def classify(df):
    results = {'numbers': [], 'non_english': [], 'unusual_proper_nouns': []}
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Classifying"):
        text = get_question_text(row)
        if not text.strip():
            continue
        if contains_number(text):
            results['numbers'].append(idx)
        if contains_non_english_and_words(text):
            results['non_english'].append(idx)
        try:
            if has_unusual_proper_nouns(text):
                results['unusual_proper_nouns'].append(idx)
        except Exception:
            pass
    return results

def sample_indices(indices, n):
    if len(indices) < n:
        raise ValueError(f"Not enough indices to sample: requested {n}, but only {len(indices)} available.")
    return random.sample(indices, n)

def save_samples(samples, df, outdir, fmt, timestamp):
    for cat, idxs in samples.items():
        if not idxs:
            continue
        outpath = outdir / f"jeopardy_ner_{cat}_{timestamp}.{fmt}"
        subset = df.iloc[idxs].reset_index(drop=True)
        if fmt == "json":
            subset.to_json(outpath, orient="records", indent=2)
        else:
            subset.to_json(outpath, orient="records", lines=True)
        print(f"Saved {len(subset)} to {outpath}")

def save_summary(df, classified, samples, outdir, timestamp):
    summary = {
        "timestamp": timestamp,
        "total_questions_analyzed": len(df),
        "categories": {
            cat: {
                "total_available": len(classified[cat]),
                "samples_created": len(samples[cat]),
                "percentage_of_total": len(classified[cat]) / len(df) * 100 if len(df) else 0
            }
            for cat in classified
        }
    }
    with open(outdir / f"curation_summary_{timestamp}.json", "w") as f:
        json.dump(summary, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Curate Jeopardy dataset for NER validation (questions only)")
    parser.add_argument('--data-dir', type=str, help='Raw data dir (default: ../data)')
    parser.add_argument('--output-dir', type=str, help='Output dir (default: ../output)')
    parser.add_argument('--sample-size', type=int, default=1000, help='Examples per category')
    parser.add_argument('--format', choices=['json', 'jsonl'], default='jsonl', help='Output format')
    args = parser.parse_args()

    random.seed(42)
    script_dir = Path(__file__).parent
    root = script_dir.parent
    data_dir = Path(args.data_dir) if args.data_dir else root / "data"
    outdir = Path(args.output_dir) if args.output_dir else root / "output"
    outdir.mkdir(parents=True, exist_ok=True)

    # Use the same filename as in data_download_and_eda.py by default
    df = load_jeopardy_data(data_dir=str(data_dir), filename='JEOPARDY_QUESTIONS1.json')

    classified = classify(df)

    samples = {}
    for cat in classified:
        try:
            samples[cat] = sample_indices(classified[cat], args.sample_size)
        except ValueError as e:
            print(f"Error for category '{cat}': {e}", file=sys.stderr)
            sys.exit(1)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_samples(samples, df, outdir, args.format, timestamp)
    save_summary(df, classified, samples, outdir, timestamp)
    print(f"\nCuration complete! Check {outdir} for output files.")

if __name__ == "__main__":
    main()