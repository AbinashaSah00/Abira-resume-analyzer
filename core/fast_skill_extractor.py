# 📄 core/fast_skill_extractor.py

import re
from llm.abeera_llm import ask_llama_local
from llm.interaction_logger import log_interaction


class FastSkillExtractor:
    
    def __init__(self, skill_list_path=None):
        pass

    def extract_skills(self, text: str, source: str = "resume") -> list:
        prompt = f"Extract all technical and soft skills from this {source} text as a simple, comma-separated list: {text}"
        response = ask_llama_local(prompt)
        log_interaction(prompt, response)

        # Clean and sanitize
        raw = response.lower()
        raw = re.sub(r'\x1b\[[0-9;]*m', '', raw)
        raw = re.sub(r'(keywords:|1\.|2\.|3\.|4\.|5\.|6\.|7\.)', '', raw)
        raw = re.sub(r'[\n\r]', ' ', raw)
        raw = re.sub(r'\s+', ' ', raw).strip()

        # Extract only comma-separated phrases, filter out long ones
        items = re.split(r',\s*', raw)
        cleaned_skills = [s.strip() for s in items if s and len(s.strip()) > 1 and len(s.strip().split()) <= 3]
        return list(set(cleaned_skills))    # Unique only
