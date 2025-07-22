"""
Tests for contains_non_english_and_words from check_for_non_english_words.py

These tests validate that the function correctly detects non-English words
in text, following the implementation in check_for_non_english_words.py.
"""

import sys
import os
import pytest

# Ensure src is in path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from check_for_non_english_words import contains_non_english_and_words

TEST_CASES = [
    # Basic English cases
    ("Hello world this is English", False),
    ("The quick brown fox jumps over the lazy dog", False),
    ("", False),
    
    # Clear non-English cases
    ("Hola mundo cómo estás", True), 
    ("Bonjour le monde français", True),
    ("Mix of English and español words", True),
    
    # Numbers should be ignored
    ("Numbers 123 and 45.67 should be ignored", False),
    ("123 456.78 $9.99", False),
    ("COVID-19 pandemic started in 2020", True),  # "COVID" not in dictionary
    ("Room 101, floor 2B, apartment 4A", True),  # Some terms not recognized
    
    # Contractions and common English patterns
    ("I can't believe it's working don't you think", False),
    ("We're going to McDonald's for dinner", False),
    ("That's John's car over there", False),
    
    # Hyphenated words - often fail because parts aren't recognized
    ("This is a well-known state-of-the-art solution", True),  # Hyphenated parts split
    ("Twenty-one year-old co-worker", True),  # Hyphenated words split
    
    # Proper nouns (places, names) - might vary by dictionary
    ("Paris London Tokyo New York", False),
    ("Shakespeare wrote Hamlet", False),
    ("Visit the Louvre Museum in Paris", False),
    
    # Words with accents commonly used in English
    ("We had café au lait and naïve discussions", True),
    ("Submit your résumé by email", True),
    ("The piñata was full of candy", True),
    
    # Scientific and technical terms
    ("DNA contains adenine guanine cytosine thymine", False),
    ("Photosynthesis occurs in chloroplasts", False),
    ("Algorithm optimization and debugging", False),
    
    # Abbreviations and acronyms
    ("NASA sent a rover to Mars via SpaceX", True),  # "SpaceX" not in dictionary
    ("The FBI and CIA work with NATO", False),
    ("Check the FAQ on our website", False),
    
    # Mixed languages clearly non-English
    ("Guten Tag, wie geht es dir heute", True),
    ("Ciao bella, come stai oggi", True),
    ("Konnichiwa, genki desu ka", True),
    
    # Edge cases with punctuation
    ("!@#$%^&*()_+-=[]{}|;':\",./<>?", False),
    ("Hello, world! How are you today?", False),
    
    # Very short texts
    ("Hi", False),
    ("OK", False),
    ("No", False),
    
    # Currency and measurements
    ("$19.99 €25.50 £15.00 ¥1000", False),
    ("5kg 10cm 25°C 100mph", True),  # Units like "kg", "mph" not in dictionary
    
    # Website/email patterns
    ("Visit example.com or email test@domain.org", False),
    ("Check http://website.com/path?param=value", True),  # URL parts not recognized
    
    # Code-like patterns
    ("function() { return true; }", False),
    ("SELECT * FROM users WHERE active = 1", False),
    
    # Borderline cases - English words that might not be in dictionary
    ("Supercalifragilisticexpialidocious is hard to spell", True),  # Made-up word not in dictionary
    ("The antiquated nomenclature requires elucidation", False),
    
    # Mixed script detection
    ("Hello мир world", True),
    ("English with 中文 characters", True),
    ("مرحبا hello world", True),
    
    # Common typos/misspellings (should still be detected as non-English)
    ("Helo wrold thsi is Englsh", True),
    ("Definately recieve seperate occured", True),
    
    # Brand names and modern terms
    ("Google Facebook Twitter Instagram", False),
    ("iPhone Android Windows MacBook", True),  # Brand names not in dictionary
    
    # Food and cultural terms
    ("Sushi ramen tempura yakitori", True),
    ("Pizza pasta gelato cappuccino", True),
    ("Tacos quesadillas nachos guacamole", False),  # These Spanish words are now in English dictionary
]

@pytest.mark.parametrize("text,expected", TEST_CASES)
def test_contains_non_english_comprehensive(text, expected):
    result = contains_non_english_and_words(text)
    assert isinstance(result, bool)
    assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])