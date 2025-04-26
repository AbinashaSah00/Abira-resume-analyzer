# Utility functions for text processing

import re

def clean_text(text):
    """
    Cleans extracted resume or JD text for comparison.

    Steps:
    - Lowercase
    - Remove extra spaces
    - Remove non-alphabetic characters (except spaces)

    Returns:
        str: Cleaned text
    """
    # Lowercase everything
    text = text.lower()

    # Remove special characters (keep only alphabets and spaces)
    text = re.sub(r'[^a-z\s]', '', text)

    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
