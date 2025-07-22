"""
Module for detecting non-English words in text using PyEnchant dictionary.
"""

import re
import enchant

# Initialize English dictionary
ENGLISH_DICT = enchant.Dict("en_US")
REGEX_NUMBER = r"^\d[\d,.-]*$"


def contains_non_english_and_words(text: str) -> bool:
    """
    Check if text contains words not found in the English dictionary.

    Args:
        text (str): The text to analyze

    Returns:
        bool: True if non-English words found, False otherwise
    """
    tokens = re.findall(r"\b\w[\w'-]*\b", text)
    for token in tokens:
        # Skip numbers to avoid false positives
        if re.fullmatch(REGEX_NUMBER, token):
            continue
        if not ENGLISH_DICT.check(token):
            return True
    return False
