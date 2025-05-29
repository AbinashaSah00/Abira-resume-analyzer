# core/skill_matcher_engine.py

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def semantic_match(skill, skill_list, threshold=0.8):
    for target_skill in skill_list:
        if similar(skill, target_skill) >= threshold:
            return target_skill
    return None

def match_skills(resume_skills, jd_skills, threshold=0.8):
    matched_skills = []
    missing_skills = []
    extra_skills = []

    # Find matched skills and missing skills
    for jd_skill in jd_skills:
        match = semantic_match(jd_skill, resume_skills, threshold)
        if match:
            matched_skills.append(jd_skill)
        else:
            missing_skills.append(jd_skill)

    # Find extra skills in resume not required by JD
    for res_skill in resume_skills:
        match = semantic_match(res_skill, jd_skills, threshold)
        if not match:
            extra_skills.append(res_skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }
