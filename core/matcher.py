# core/matcher.py

def calculate_match(resume_text, jd_skills):
    """
    Calculate match percentage between resume content and JD skills dynamically.
    """
    resume_words = set(resume_text.lower().split())
    matched_skills = resume_words.intersection(set(jd_skills))
    match_percentage = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 0
    return match_percentage, list(matched_skills)
