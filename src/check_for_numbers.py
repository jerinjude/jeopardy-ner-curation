import re

def contains_number(text: str) -> bool:
    """
    Returns True if the input text contains at least one digit, else False.

    Args:
        text (str): The input text.

    Returns:
        bool: True if text contains a digit, else False.
    """
    text = text.strip()
    return bool(re.search(r'\d', text))
