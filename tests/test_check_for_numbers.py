"""
Tests for contains_number from check_for_numbers.py

These tests validate that the function correctly detects digits
in text, following the implementation in check_for_numbers.py.
"""

import sys
import os
import pytest

# Ensure src is in path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from check_for_numbers import contains_number

TEST_CASES = [
    # Basic cases with no numbers
    ("Hello world", False),
    ("The quick brown fox jumps over the lazy dog", False),
    ("", False),
    ("No digits here at all", False),
    
    # Basic cases with numbers
    ("There are 5 cats", True),
    ("I have 123 apples", True),
    ("The year 2024", True),
    ("Just 1", True),
    
    # Numbers at different positions
    ("1 at the start", True),
    ("At the end 9", True),
    ("In the 5 middle", True),
    ("Multiple 1 and 2 and 3", True),
    
    # Different number formats
    ("Price is $19.99", True),
    ("Temperature -25°C", True),
    ("Percentage 75%", True),
    ("Phone 555-1234", True),
    ("Version 2.5.1", True),
    ("IP address 192.168.1.1", True),
    
    # Large numbers
    ("Population 7,894,000,000", True),
    ("Scientific notation 6.022e23", True),
    ("Very long 123456789012345", True),
    
    # Numbers with words
    ("COVID-19 pandemic", True),
    ("Windows 10 or Windows 11", True),
    ("iPhone 15 Pro Max", True),
    ("Room 101B", True),
    
    # Fractions and decimals
    ("About 3.14159 pi", True),
    ("Fraction 1/2 cup", True),
    ("Ratio 16:9 screen", True),
    ("Score 98.5 out of 100", True),
    
    # Time and dates
    ("Meeting at 3:30 PM", True),
    ("Born on 12/25/1990", True),
    ("Year 2024 January 1st", True),
    ("24-hour format 23:59", True),
    
    # Currencies from different countries
    ("$1,234.56 USD", True),
    ("€99.99 EUR", True),
    ("£45.00 GBP", True),
    ("¥1000 JPY", True),
    ("₹500 INR", True),
    
    # Measurements and units
    ("5kg weight", True),
    ("100mph speed", True),
    ("25°C temperature", True),
    ("6 feet tall", True),
    ("500ml bottle", True),
    
    # Technical contexts
    ("HTTP status 404", True),
    ("Port 8080", True),
    ("64-bit processor", True),
    ("1TB storage", True),
    ("4K resolution", True),
    
    # Mathematical expressions
    ("2 + 2 = 4", True),
    ("Square root of 16", True),
    ("Formula E=mc²", False),  # Unicode ² character not matched by \d
    ("Angle 90 degrees", True),
    
    # Dates in different formats
    ("1st January 2024", True),
    ("Jan 1, 2024", True),
    ("2024-01-01", True),
    ("01/01/24", True),
    
    # Sports scores and statistics
    ("Final score 3-2", True),
    ("Batting average .325", True),
    ("Rank #1 player", True),
    ("Season 2023-24", True),
    
    # Web and tech formats
    ("Website example.com/page1", True),
    ("Email user123@domain.com", True),
    ("Password must have 8 characters", True),
    ("Download v2.0 here", True),
    
    # Edge cases with whitespace
    ("   5   ", True),
    ("\t\n1\r\n", True),
    ("  No numbers here  ", False),
    
    # Unicode digits (should still match with \d)
    ("Unicode digit ５", True),  # Full-width 5
    ("Arabic digit ٧", True),   # Arabic-Indic digit 7
    ("Devanagari digit ४", True), # Devanagari digit 4
    
    # Mixed with punctuation
    ("Price: $25.99!", True),
    ("Question #3?", True),
    ("List: (1) first item", True),
    ("Note [2]: important", True),
    
    # Numbers spelled out (should be False)
    ("I have five cats", False),
    ("Twenty-one years old", False),
    ("One hundred percent", False),
    ("First place winner", False),
    
    # Roman numerals (should be False as they're letters)
    ("Chapter IV", False),
    ("World War II", False),
    ("Louis XIV", False),
    ("Super Bowl LVII", False),
    
    # Only punctuation and symbols
    ("!@#$%^&*()", False),
    (".,;:!?", False),
    ("+-*/=", False),
    ("()[]{}\"'", False),
    
    # Single characters
    ("5", True),
    ("a", False),
    ("!", False),
    (" ", False),
]

@pytest.mark.parametrize("text,expected", TEST_CASES)
def test_contains_number_comprehensive(text, expected):
    result = contains_number(text)
    assert isinstance(result, bool)
    assert result == expected

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 