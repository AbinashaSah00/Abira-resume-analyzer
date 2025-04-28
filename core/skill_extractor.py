# core/skill_extractor.py

import re

def extract_skills_from_jd(jd_text):
    """
    Dynamically extract potential skills or keywords from a job description.
    """
    # Extract all words
    words = re.findall(r'\b[A-Za-z]+\b', jd_text)

    # Filter out small/common words
    filtered = [word for word in words if len(word) > 2]

    # Normalize: lower case and deduplicate
    unique_skills = list(set(word.lower() for word in filtered))

    return unique_skills