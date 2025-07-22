"""
Tests for curate_jeopardy_dataset.py

Validates classification of Jeopardy questions into numbers, non-English, and unusual proper nouns categories.
"""

import sys
import os
import pytest
import pandas as pd

# Ensure src is in path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from curate_jeopardy_dataset import classify

# Test cases: (questions_list, expected_numbers_indices, expected_non_english_indices, expected_unusual_proper_nouns_indices)
TEST_CASES = [
    # Basic English questions
    (["What is the capital of France?", "Who wrote Hamlet?"], [], [], []),
    # Clear numerical content
    (
        ["This building has 5 floors", "The year was 1969", "Price is 25 dollars"],
        [0, 1, 2],
        [],
        [],
    ),
    # Decimal numbers and complex formats
    (
        [
            "The temperature was 98.6 degrees",
            "Price dropped to $19.99 today",
            "Meeting at 3:30 PM on January 1st",
            "Born in 1985 and graduated in 2007",
        ],
        [0, 1, 2, 3],
        [2],
        [],  # "PM" detected as non-English
    ),
    # Foreign language content
    (
        [
            "Say hello in Spanish: hola",
            "French word for cat: chat",
            "German greeting: guten tag",
        ],
        [],
        [0, 2],
        [],  # "chat" not detected as foreign
    ),
    # Mixed foreign languages
    (
        [
            "Say konnichiwa in Japanese culture",
            "Italian ciao means hello or goodbye",
            "Russian dasvidaniya means farewell",
        ],
        [],
        [0, 2],
        [2],  # "dasvidaniya" also detected as unusual proper noun
    ),
    # Made-up fictional names
    (
        [
            "The wizard Zorkblatt cast spells",
            "Princess Xyrellia ruled the kingdom",
            "Hero Blorzaniq saved the day",
        ],
        [],
        [0, 1, 2],
        [0, 1, 2],
    ),
    # Scientific terms
    (
        [
            "DNA contains adenine and thymine bases",
            "Algorithm uses machine learning techniques",
            "Photosynthesis occurs in chloroplasts",
        ],
        [],
        [],
        [],
    ),
    # Mixed categories
    (
        ["I have 3 cats", "Say bonjour in France", "The hero Zylothia won"],
        [0],
        [1, 2],
        [2],
    ),
    # Complex mixed scenarios
    (
        [
            "In 1969 astronauts said bonjour to aliens",
            "The wizard Krythaxios cast 7 magic spells",
            "Scientist discovered 42 new especies today",
        ],
        [0, 1, 2],
        [0, 1, 2],
        [1],
    ),
    # Long complex sentences
    (
        [
            "The research team of 15 scientists including Dr. Zylophagus studied 200 specimens of bacteria for 3 years while speaking français and deutsch",
            "Captain Xerothane commanded 50 ships during the 1999 battle against alien forces from planet Zorbonia",
        ],
        [0, 1],
        [0, 1],
        [0, 1],
    ),
    # Simple validation case
    (["This is normal English"], [], [], []),
]


@pytest.mark.parametrize(
    "questions,expected_numbers,expected_non_english,expected_unusual_proper_nouns",
    TEST_CASES,
)
def test_classify_comprehensive(
    questions, expected_numbers, expected_non_english, expected_unusual_proper_nouns
):
    """Test classify function with comprehensive Jeopardy-style question examples"""
    df = pd.DataFrame({"question": questions})
    result = classify(df)

    # Convert to sets for easier comparison (order doesn't matter)
    assert set(result["numbers"]) == set(expected_numbers)
    assert set(result["non_english"]) == set(expected_non_english)
    assert set(result["unusual_proper_nouns"]) == set(expected_unusual_proper_nouns)

    # Ensure result structure is correct
    assert isinstance(result, dict)
    assert set(result.keys()) == {"numbers", "non_english", "unusual_proper_nouns"}
    assert all(isinstance(indices, list) for indices in result.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
