#core/skill_gap_detector.py

import json
import re
from llm.abeera_llm import ask_llama_local
from llm.interaction_logger import log_interaction

class SkillGapDetector:
    def __init__(self, jd_skills: list, resume_skills: list):
        self.jd_skills = jd_skills
        self.resume_skills = resume_skills

    def gap_summary(self) -> dict:
        """
        Uses local LLM to classify skills into matched, partial, and missing.
        Returns a structured summary dictionary.
        """
        jd_str = ", ".join(self.jd_skills)
        resume_str = ", ".join(self.resume_skills)

        prompt = f"""
Compare the two skill lists below. For each JD skill, classify it as one of:
- "matched" if it is clearly present in the resume
- "partial" if it is similar or related
- "missing" if it’s not present at all

Respond ONLY in the following JSON format:

{{
  "matched": ["sql", "python"],
  "partial": ["communication"],
  "missing": ["azure", "json"]
}}

DO NOT use placeholders like "skill1" or "skill2". Just return valid JSON using the actual JD skill names.

JD Skills: [{jd_str}]
Resume Skills: [{resume_str}]
"""


        response = ask_llama_local(prompt)
        log_interaction(prompt, response)

        # Debugging raw LLM output
        print("\n🔎 LLM Raw Output:\n", response)

        try:
            json_str = self._extract_json_block(response)
            parsed = json.loads(json_str)
            return {
                "fully_matched": parsed.get("matched", []),
                "partial_matches": parsed.get("partial", []),
                "missing": parsed.get("missing", []),
                "recommended_gaps": parsed.get("missing", []) + parsed.get("partial", [])
            }
        except Exception as e:
            return {
                "fully_matched": [],
                "partial_matches": [],
                "missing": [],
                "recommended_gaps": [],
                "error": f"[Parsing Error] {e}"
            }

    def _extract_json_block(self, text: str) -> str:
        """
        Extracts the first valid flat JSON object with lists of strings only.
        """
        json_candidates = re.findall(r'\{.*?\}', text, re.DOTALL)

        for candidate in json_candidates:
            try:
                parsed = json.loads(candidate)
                # Validate it's a flat dictionary with only list-of-strings
                if all(
                    isinstance(v, list) and all(isinstance(i, str) for i in v)
                    for v in parsed.values()
                ):
                    return json.dumps(parsed)
            except json.JSONDecodeError:
                continue

        raise ValueError("No valid flat JSON object with lists of strings found.")
