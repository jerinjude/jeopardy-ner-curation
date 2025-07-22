#!/usr/bin/env python3
"""
Number Detection Utilities

Detects numeric content in text strings for NER filtering.
"""

import re


def contains_number(text: str) -> bool:
    """
    Check if text contains at least one digit character.

    Args:
        text (str): Input text to analyze

    Returns:
        bool: True if text contains digits, False otherwise
    """
    text = text.strip()
    return bool(re.search(r"\d", text))
