"""
Tests for has_unusual_proper_nouns from check_for_unusual_proper_nouns.py

These tests validate that the function correctly detects unusual proper nouns
using spaCy POS tagging and wordfreq global frequency analysis.

This file also includes a utility to help find the best threshold for
has_unusual_proper_nouns by evaluating accuracy across a range of thresholds.
"""

import sys
import os
import pytest

# Ensure src is in path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from check_for_unusual_proper_nouns import has_unusual_proper_nouns, nlp
    SPACY_AVAILABLE = nlp is not None
except Exception:
    SPACY_AVAILABLE = False

# Skip all tests if spaCy model is not available
pytestmark = pytest.mark.skipif(
    not SPACY_AVAILABLE,
    reason="spaCy model 'en_core_web_sm' not available. Install with: python -m spacy download en_core_web_sm"
)

TEST_CASES = [
    # Basic cases - empty/simple
    ("", False),
    ("   ", False),
    ("hello world, this is a simple sentence.", False),
    ("the quick brown fox jumps over the lazy dog in the park.", False),

    # Common proper nouns (should be False - high frequency)
    ("John went to New York for a business meeting and enjoyed the city lights.", False),
    ("Mary lives in London and often visits the British Museum on weekends.", False),
    ("We decided to visit Paris and France during our summer vacation.", False),
    ("Microsoft and Apple are two of the biggest tech companies in the world.", False),
    ("President Obama gave a speech at the White House in Washington.", False),
    ("Jesus Christ is a central figure in Christianity and is known worldwide.", False),

    # Mix of common and potentially unusual
    ("Shakespeare wrote Hamlet, which is considered one of the greatest plays ever.", False),
    ("Einstein discovered relativity and changed the way we understand physics.", False),
    ("During our trip, we decided to visit Tokyo and Japan for the cherry blossoms.", False),

    # Potentially unusual proper nouns (results may vary)
    ("Bartłomiej Kisielewski was born in Kraków and later moved to Warsaw for university.", True),
    ("Xylocarpus granatum grows in Sundarbans, a unique mangrove forest in South Asia.", True),
    ("We visited Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch, the famous Welsh town with the longest name.", True),
    ("Thuwaybah nursed the Prophet and played a significant role in early Islamic history.", True),

    # Technical/scientific terms that might be proper nouns
    ("Escherichia coli bacteria are commonly used in laboratory experiments for genetic research.", True),
    ("Homo sapiens evolution is a topic discussed in many anthropology courses worldwide.", False),
    ("The Tyrannosaurus rex fossil was discovered in the remote Badlands of Montana.", True),

    # Fictional characters (might vary)
    ("Harry Potter at Hogwarts learned magic and fought against Voldemort with his friends.", False),
    ("Hermione Granger cast spells and helped Harry and Ron solve mysteries at school.", False),
    ("Zorbonx defeated Kythara in the final battle of the intergalactic saga.", True),

    # Geographic locations
    ("Timbuktu in Mali, Africa, is known for its ancient manuscripts and desert landscape.", True),
    ("Ouagadougou, the capital of Burkina Faso, is famous for its vibrant culture.", True),

    # Historical figures
    ("Napoleon Bonaparte, the Emperor of France, led many military campaigns across Europe.", False),
    ("Julius Caesar ruled Rome and played a critical role in the rise of the Roman Empire.", False),
    ("Diocles was a famous charioteer in ancient Rome, celebrated for his victories.", False),

    # Modern celebrities/brands
    ("Elon Musk founded Tesla and SpaceX, revolutionizing electric cars and space travel.", False),
    ("Taylor Swift performed at a sold-out concert in New York City last night.", False),
    ("Zendaya Coleman, a talented actress, received an award for her outstanding performance.", True),

    # Mixed script and international names
    ("Владимир Putin from Russia attended the international summit in Geneva.", True),
    ("الملك عبدالله of Saudi Arabia was known for his reforms and leadership.", True),

    # Multiple proper nouns
    ("John, Mary, Peter, and Susan went on a road trip across the United States.", False),
    ("Zorkblatt, Xynthia, and Qwardian formed a new alliance in the fantasy novel.", True),
    ("John went to Zorkington, a mysterious town mentioned in old legends.", True),

    # Business/organization names
    ("Google, Facebook, and Amazon dominate the global technology market.", False),
    ("UNESCO, UNICEF, and WHO are important international organizations.", False),
    ("Zyntherex Corporation announced a breakthrough in pharmaceutical research.", True),

    # Academic/scientific institutions
    ("Harvard University and MIT collaborate on cutting-edge research projects.", False),
    ("Stanford, Berkeley, and UCLA are top universities in California.", False),
    ("Borbonicus Institute published a new study on quantum computing.", True),

    # Religious/mythological names
    ("Zeus, Apollo, and Athena are prominent gods in Greek mythology.", False),
    ("Buddha, Krishna, and Shiva are revered figures in world religions.", False),
    ("Xerthak, the god of storms, was worshipped by the ancient tribe.", True),

    # Literary references
    ("Sherlock Holmes and Watson solved many mysteries in Victorian London.", False),
    ("Gatsby, Daisy, and Buchanan are central characters in The Great Gatsby.", False),
    ("Zephyrius Blackthorne embarked on a perilous quest in the new fantasy series.", True),

    # Sports figures
    ("Messi and Ronaldo are considered two of the greatest football players of all time.", False),
    ("LeBron James is a basketball legend who has won multiple NBA championships.", False),
    ("Zorbinski, the tennis player, shocked the world by winning the Grand Slam.", True),

    # Edge cases with punctuation
    ("Dr. John Smith presented his research at the international conference.", False),
    ("Mr. Zorkblattsson delivered a keynote speech at the annual summit.", True),
    ("St. Patrick's Day is celebrated with parades and green attire.", False),

    # Abbreviations and acronyms (might not be tagged as PROPN)
    ("IBM's CEO announced a new initiative for artificial intelligence.", False),
    ("FBI, CIA, and NSA are agencies responsible for national security.", False),
    ("XYZ Corp and ABC Inc merged to form a new conglomerate.", True),

    # Numbers with proper nouns
    ("John Smith, born in 1980, is a well-known author and speaker.", False),
    ("Zorkblatt, who won 456 awards, is a legend in his field.", True),

    # Case sensitivity tests
    ("john smith is a common name found in many countries.", False),
    ("JOHN SMITH was mentioned in the report as a key witness.", False),
    ("zorkblatt xynthia are characters from a lesser-known science fiction novel.", True),
]

@pytest.mark.parametrize("text,expected", TEST_CASES)
def test_has_unusual_proper_nouns(text, expected):
    """
    Test has_unusual_proper_nouns with a variety of cases.
    Note: Some results may depend on the wordfreq database version.
    """
    result = has_unusual_proper_nouns(text)
    assert isinstance(result, bool)
    assert result == expected

@pytest.mark.parametrize("threshold", [1e-9, 1e-6, 1e-3, 1e-1])
def test_different_thresholds(threshold):
    """Test function behavior with different threshold values."""
    text = "Napoleon Bonaparte conquered Europe"
    result = has_unusual_proper_nouns(text, global_rare_threshold=threshold)
    assert isinstance(result, bool)

def find_best_threshold(test_cases, thresholds=None, verbose=True):
    """
    Try different thresholds, track metrics, and select the best one.
    Prints the best threshold and its metrics.
    Returns the best threshold and a list of (threshold, accuracy, precision, recall, f1, false_positives, false_negatives).
    """
    if thresholds is None:
        # Logarithmic scale from 1e-10 to 1e-2
        thresholds = [10**exp for exp in range(-10, -1)]
        thresholds += [5e-7, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]
        thresholds = sorted(set(thresholds))
    results = []
    best_metric = -1
    best_threshold = None
    best_metrics = None
    for threshold in thresholds:
        tp = 0  # True positives
        tn = 0  # True negatives
        fp = 0  # False positives
        fn = 0  # False negatives
        for text, expected in test_cases:
            try:
                result = has_unusual_proper_nouns(text, global_rare_threshold=threshold)
            except Exception:
                continue
            if result and expected:
                tp += 1
            elif not result and not expected:
                tn += 1
            elif result and not expected:
                fp += 1
            elif not result and expected:
                fn += 1
        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total if total else 0.0
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        results.append((threshold, accuracy, precision, recall, f1, fp, fn))
        if verbose:
            print(f"Threshold: {threshold:.1e} | Acc: {accuracy:.3f} | Prec: {precision:.3f} | Rec: {recall:.3f} | F1: {f1:.3f} | FP: {fp} | FN: {fn}")
        # Use F1 as the main metric for "best"
        if f1 > best_metric:
            best_metric = f1
            best_threshold = threshold
            best_metrics = (accuracy, precision, recall, f1, fp, fn)
    if verbose and best_threshold is not None:
        print(f"\nBest threshold: {best_threshold:.1e}")
        print(f"  Accuracy:  {best_metrics[0]:.3f}")
        print(f"  Precision: {best_metrics[1]:.3f}")
        print(f"  Recall:    {best_metrics[2]:.3f}")
        print(f"  F1:        {best_metrics[3]:.3f}")
        print(f"  FP:        {best_metrics[4]}")
        print(f"  FN:        {best_metrics[5]}")
    return best_threshold, results

if __name__ == "__main__":
    if not SPACY_AVAILABLE:
        print("spaCy model 'en_core_web_sm' not available.")
        print("Install with: python -m spacy download en_core_web_sm")
    else:
        import argparse
        parser = argparse.ArgumentParser(description="Test has_unusual_proper_nouns and find the best threshold.")
        parser.add_argument("--find-threshold", action="store_true", help="Try different thresholds and print accuracy and metrics.")
        parser.add_argument("--pytest", action="store_true", help="Run pytest as usual.")
        args = parser.parse_args()
        if args.find_threshold:
            print("Trying different thresholds to find the best one (by F1 score)...")
            best_threshold, all_results = find_best_threshold(TEST_CASES)
            print(f"Best threshold found: {best_threshold}")
        elif args.pytest:
            pytest.main([__file__, "-v"])
        else:
            print("Specify --find-threshold to try thresholds or --pytest to run tests.")