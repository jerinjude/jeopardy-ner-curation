# Jeopardy NER Curation Pipeline

A Python pipeline that curates Jeopardy questions into three datasets for Named Entity Recognition validation.

## Overview

This script processes the Jeopardy Questions dataset and creates three curated subsets:

- **Numbers**: Questions containing numerical values, dates, scores
- **Non-English Words**: Questions with foreign words or transliterations  
- **Unusual Proper Nouns**: Questions with rare names, places, or terminology

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

```bash
cd src
python curate_jeopardy_dataset.py
```

This will:
- Download the Jeopardy dataset if needed
- Create 1000 examples for each category
- Export datasets as JSONL files to ../output/

### Options

```bash
python curate_jeopardy_dataset.py --sample-size 500  # Smaller datasets
python curate_jeopardy_dataset.py --format json     # JSON format
```

## Project Structure

```
src/
├── curate_jeopardy_dataset.py         # Main script
├── data_download_and_eda.py           # Data loading
├── check_for_numbers.py               # Numbers detection
├── check_for_non_english_words.py     # Non-English detection
└── check_for_unusual_proper_nouns.py  # Proper nouns detection

tests/
├── test_curate_jeopardy_dataset.py
├── test_check_for_numbers.py
├── test_check_for_non_english_words.py
└── test_check_for_unusual_proper_nouns.py
```

## Testing

```bash
python -m pytest tests/ -v
```

## Dependencies

- pandas: Data manipulation
- spacy: NLP processing  
- pyenchant: English dictionary
- wordfreq: Word frequency analysis
- gdown: Google Drive downloads
- tqdm: Progress bars