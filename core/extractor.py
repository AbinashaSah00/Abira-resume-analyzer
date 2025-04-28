import re

def extract_email(text):
    """Extracts the first email found in the given text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text):
    """Extracts the first 10-digit phone number found in the given text."""
    phone_pattern = r'\b\d{10}\b'
    matches = re.findall(phone_pattern, text)
    return matches[0] if matches else None

def extract_skills(text, skills_database):
    extracted_skills = []
    text_lower = text.lower()
    for skill in skills_database:
        if skill.lower() in text_lower:
            extracted_skills.append(skill)
    return extracted_skills

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

# core/extractor.py

import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
