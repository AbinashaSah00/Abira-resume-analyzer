#core/profile_scorecard.py

import re
import json
from llm.abeera_llm import ask_llama_local
from llm.interaction_logger import log_interaction

def compute_profile_score(
    jd_titles: list,
    resume_titles: list,
    jd_skills: list,
    resume_skills: list,
    experience_years: float,
    jd_degrees: list,
    resume_degrees: list
) -> dict:
    """
    Asks LLM to extract profile facts, then scores based on heuristics.
    """

    jd_title_str = ", ".join(jd_titles)
    resume_title_str = ", ".join(resume_titles)
    jd_skills_str = ", ".join(jd_skills)
    resume_skills_str = ", ".join(resume_skills)
    edu_str = f"JD: {', '.join(jd_degrees)} | Resume: {', '.join(resume_degrees)}"

    prompt = f"""
From the following inputs, extract normalized candidate profile facts for scoring.
Respond ONLY in JSON format like this:

{{
  "title_match": "low | moderate | high",
  "experience_years": 1.5,
  "education": {{ "jd_degree": "b.tech", "resume_degree": "bba" }},
  "skills": {{ "matched": [...], "missing": [...] }},
  "tools": [...]
}}

Inputs:
JD Titles: {jd_title_str}
Resume Titles: {resume_title_str}
JD Skills: {jd_skills_str}
Resume Skills: {resume_skills_str}
Experience Years: {experience_years}
JD Degree(s): {', '.join(jd_degrees)}
Resume Degree(s): {', '.join(resume_degrees)}
"""

    print("\n📝 LLM Prompt Sent:\n", prompt)

    response = ask_llama_local(prompt)
    log_interaction(prompt, response)

    print("\n📊 Raw LLM Extracted Facts:\n", response)

    # Try basic key matching manually if JSON parse fails
    try:
        facts = _extract_facts_fallback(response)

        score = {
            "title_match": {"low": 5, "moderate": 12, "high": 20}.get(facts.get("title_match", "low"), 0),
            "experience_duration": min(round(float(facts.get("experience_years", 0)) * 10), 20),
            "skills": min(len(facts.get("skills", {}).get("matched", [])) * 8, 40),
            "tools": min(len(facts.get("tools", [])) * 2, 10),
            "education_match": 10 if facts.get("education", {}).get("jd_degree", "").lower()[:3] == facts.get("education", {}).get("resume_degree", "").lower()[:3] else 5
        }
        score["total"] = sum(score.values())

        return {
            "scores": score,
            "explanation": "Scored using fallback extraction from LLM output"
        }

    except Exception as e:
        return {
            "scores": {
                "title_match": 0,
                "experience_duration": 0,
                "skills": 0,
                "tools": 0,
                "education_match": 0,
                "total": 0
            },
            "explanation": f"Failed to extract profile facts: {e}"
        }

def _extract_facts_fallback(text: str) -> dict:
    """
    Extract facts from messy LLM response using regex fallback
    """
    facts = {
        "title_match": "low",
        "experience_years": 0.0,
        "education": {"jd_degree": "", "resume_degree": ""},
        "skills": {"matched": [], "missing": []},
        "tools": []
    }

    if re.search(r"title[_\s]*match[^:]*high", text, re.I):
        facts["title_match"] = "high"
    elif re.search(r"title[_\s]*match[^:]*moderate", text, re.I):
        facts["title_match"] = "moderate"

    exp_match = re.search(r"experience[_\s]*years[^:]*[:\s]*([\d\.]+)", text, re.I)
    if exp_match:
        facts["experience_years"] = float(exp_match.group(1))

    edu_match = re.search(r'education[^:]*\{[^}]*"jd_degree":\s*"([^"]+)",\s*"resume_degree":\s*"([^"]+)"', text, re.I)
    if edu_match:
        facts["education"]["jd_degree"] = edu_match.group(1)
        facts["education"]["resume_degree"] = edu_match.group(2)

    matched_skills = re.findall(r'"matched"\s*:\s*\[(.*?)\]', text, re.DOTALL)
    if matched_skills:
        skills_raw = matched_skills[0]
        skills = re.findall(r'"(.*?)"', skills_raw)
        facts["skills"]["matched"] = skills

    tools_match = re.search(r'"tools"\s*:\s*\[(.*?)\]', text, re.DOTALL)
    if tools_match:
        tool_list = re.findall(r'"(.*?)"', tools_match.group(1))
        facts["tools"] = tool_list

    return facts
