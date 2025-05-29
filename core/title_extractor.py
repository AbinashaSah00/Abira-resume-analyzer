import re
from llm.abeera_llm import ask_llama_local
from llm.interaction_logger import log_interaction

class TitleExtractor:
    def __init__(self, bank_path=None):
        pass

    def extract(self, text: str, source: str = "jd") -> tuple:
        """
        Extracts the most likely job title using local LLM.
        Returns (title: str, score: float, method: str)
        """
        prompt = f"""
Extract the most appropriate job title from the following {source.upper()} text.
Respond with only the job title in lowercase — no punctuation, no location, no company name, no explanation.
Just return the title only. One line.

Text:
{text}
"""

        response = ask_llama_local(prompt)
        log_interaction(prompt, response)

        # Step 1: Normalize and clean
        raw = response.strip().lower()
        raw = re.sub(r'[^\w\s\-]', '', raw)  # remove punctuation
        raw = raw.split("\n")[0]

        # Step 2: Use regex to match a probable title (1-6 words)
        match = re.search(r'\b(?:[a-z]{2,}\s){0,5}[a-z]{2,}\b', raw)
        cleaned_title = match.group(0).strip() if match else "unknown"

        # Step 3: Remove common prefixes like 'job title', 'role', etc.
        cleaned_title = re.sub(r'^(job title|role)[:\- ]*', '', cleaned_title).strip()

        return (cleaned_title, 1.0, "llm-inferred")
