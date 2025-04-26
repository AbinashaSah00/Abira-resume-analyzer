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