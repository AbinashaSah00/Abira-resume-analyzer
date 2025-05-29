import re

def extract_required_degrees(jd_text):
    """
    Extract required degree mentions from JD.
    Returns a list of (degree, field) tuples.
    """
    patterns = [
        r"(bachelor(?:'s)?|b\.?tech)\s+(of|in)?\s*([\w\s&]+)?",
        r"(master(?:'s)?|m\.?tech|m\.?sc)\s+(of|in)?\s*([\w\s&]+)?",
        r"(ph\.?d|doctorate)\s+(of|in)?\s*([\w\s&]+)?"
    ]
    matches = []
    for pat in patterns:
        found = re.findall(pat, jd_text.lower())
        for degree, _, field in found:
            matches.append((degree.replace('.', ''), field.strip()))
    return matches
