#!/usr/bin/env python3
"""
Unusual Proper Noun Detection Module

Detects rare proper nouns using spaCy POS tagging and wordfreq analysis.
"""

import spacy
from wordfreq import word_frequency

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None


def has_unusual_proper_nouns(text: str, global_rare_threshold: float = 1e-6) -> bool:
    """
    Check if text contains unusual proper nouns based on global frequency.

    Args:
        text (str): Input text to analyze
        global_rare_threshold (float): Frequency threshold for unusual classification

    Returns:
        bool: True if unusual proper nouns found, False otherwise

    Raises:
        ValueError: If spaCy model not available
    """
    if not nlp:
        raise ValueError(
            "spaCy model not available. Please install with:\n"
            "python -m spacy download en_core_web_sm"
        )

    if not text or not text.strip():
        return False

    doc = nlp(text)

    for token in doc:
        if token.pos_ == "PROPN" and len(token.text) >= 3 and token.is_alpha:

            global_freq = word_frequency(
                token.text.lower(), "en", wordlist="best", minimum=0.0
            )

            if global_freq < global_rare_threshold:
                return True

    return False
