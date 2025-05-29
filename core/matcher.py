# core/matcher.py (inside your skill gap logic)
from core.semantic_matcher import get_best_match

def match_skills(jd_skills, resume_skills):
    matched = []
    partial = []
    missing = []

    for jd_skill in jd_skills:
        jd_lower = jd_skill.lower()
        if jd_lower in [s.lower() for s in resume_skills]:
            matched.append(jd_skill)
        else:
            best_match, score = get_best_match(jd_lower, resume_skills)
            if best_match:
                partial.append((jd_skill, best_match, score))
            else:
                missing.append(jd_skill)
    
    return matched, partial, missing
