"""
Module for detecting non-English words in text.

This module provides utilities to check if text contains words that are not
found in the English dictionary, which can be useful for filtering or 
identifying foreign language content.
"""

import re
import enchant

# Initialize English dictionary
ENGLISH_DICT = enchant.Dict("en_US")


def contains_non_english_and_words(text: str) -> tuple[bool, list[str]]:
    """
    Check if text contains words not found in the English dictionary,
    and return both the boolean result and the list of such words.

    Args:
        text (str): The text to analyze

    Returns:
        tuple[bool, list[str]]: (True if non-English words found, list of those words)
    """
    non_english_words = []
    tokens = re.findall(r"\b\w[\w'-]*\b", text)
    for token in tokens:
        if not ENGLISH_DICT.check(token.lower()):
            non_english_words.append(token)
    return (len(non_english_words) > 0, non_english_words)
