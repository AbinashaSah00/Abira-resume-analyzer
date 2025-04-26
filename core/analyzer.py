# analyzer.py

def match_skills(resume_text, required_skills):
    """
    Compares resume text with a list of required skills and returns match percentage.
    """
    matched_skills = []
    resume_text_lower = resume_text.lower()
    unmatched = []
    
    for skill in required_skills:
        if skill.lower() in resume_text_lower:
            matched_skills.append(skill)
        else:
            unmatched.append(skill)
    
    match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
    
    return round(match_percentage,'%', 2), unmatched
