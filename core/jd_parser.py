# Code to extract job description keywords

# jd_parser.py

def extract_skills_from_jd(jd_text, skills_database):
    """
    Extracts relevant skills from job description text based on a skills database.
    """
    jd_text_lower = jd_text.lower()
    extracted_skills = []
    
    for skill in skills_database:
        if skill.lower() in jd_text_lower:
            extracted_skills.append(skill)
    
    return extracted_skills
