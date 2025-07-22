import spacy
from wordfreq import word_frequency

# Load spaCy English model once globally
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None  # User must download with: python -m spacy download en_core_web_sm


def has_unusual_proper_nouns(text: str, global_rare_threshold: float = 1e-6) -> bool:
    """
    Check if text contains unusual proper nouns based on global frequency analysis.
    
    Uses spaCy POS tagging to identify proper nouns, then checks their global 
    frequency using wordfreq to determine if any are unusual/rare.
    
    Args:
        text: Input text to analyze
        global_rare_threshold: Frequency threshold below which a proper noun 
                             is considered unusual (default: 1e-6)
    
    Returns:
        bool: True if text contains unusual proper nouns, False otherwise
    
    Raises:
        ValueError: If spaCy model is not available
    """
    if not nlp:
        raise ValueError(
            "spaCy model not available. Please install with:\n"
            "python -m spacy download en_core_web_sm"
        )
    
    if not text or not text.strip():
        return False
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Find all proper nouns
    for token in doc:
        if (token.pos_ == 'PROPN' and 
            len(token.text) >= 3 and 
            token.is_alpha):
            
            # Check global frequency
            global_freq = word_frequency(token.text.lower(), 'en', wordlist='best', minimum=0.0)
            
            # If this proper noun is globally rare, text has unusual proper nouns
            if global_freq < global_rare_threshold:
                return True
    
    return False
