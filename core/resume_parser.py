# core/resume_parser.py

import fitz  # PyMuPDF
import re
from datetime import datetime

class ResumeParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self._load_text()

    def _load_text(self):
        """Extracts raw text from a resume PDF."""
        try:
            with fitz.open(self.file_path) as doc:
                self.text = "\n".join(page.get_text() for page in doc)
        except Exception as e:
            print(f"[ERROR] Failed to extract resume text: {e}")
            self.text = ""

    def extract_text(self):
        """Returns the resume text (used in main pipeline)."""
        return self.text.strip()

    def extract_sentences(self):
        """Basic sentence tokenizer (period-based)."""
        if not self.text:
            return []
        return re.split(r'(?<=[.!?]) +', self.text.strip())

    def extract_experience_titles(self):
        """
        Extracts job titles from experience sections using simple heuristics.
        Returns a list of dicts: [{'title': 'Data Analyst'}, ...]
        """
        titles = []
        lines = self.text.splitlines()
        for line in lines:
            if any(word in line.lower() for word in ["analyst", "manager", "scientist", "developer", "engineer", "consultant", "intern"]):
                if 3 <= len(line.split()) <= 8:
                    titles.append({"title": line.strip()})
        return titles

    def get_total_experience_years(self):
        """
        Uses regex to extract date ranges and estimate total experience in years.
        Looks for patterns like:
        - Jan 2020 – Mar 2023
        - 2019 - 2021
        - April 2018 to Present
        """
        patterns = [
            r'(?i)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–to]+\s*(Present|\d{4})',
            r'\d{4}\s*[-–to]+\s*(Present|\d{4})'
        ]
        matches = []
        for pattern in patterns:
            matches.extend(re.findall(pattern, self.text))

        total_months = 0
        for match in matches:
            try:
                start_str, end_str = match
                start_year = int(re.search(r'\d{4}', start_str).group())
                start_date = datetime(start_year, 1, 1)

                if end_str.lower() == "present":
                    end_date = datetime.today()
                else:
                    end_year = int(re.search(r'\d{4}', end_str).group())
                    end_date = datetime(end_year, 1, 1)

                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                if 0 <= months <= 600:
                    total_months += months
            except:
                continue

        return round(total_months / 12, 1) if total_months > 0 else 0


    def extract_education_entries(self):
        """
        Extract education lines containing degrees + fields.
        Returns a list like: [{'degree': 'bachelor', 'field': 'computer science'}]
        """
        education = []
        patterns = [
            r"(bachelor(?:'s)?|b\.?tech)\s+(of|in)?\s*([\w\s&]+)?",
            r"(master(?:'s)?|m\.?tech|m\.?sc)\s+(of|in)?\s*([\w\s&]+)?",
            r"(ph\.?d|doctorate)\s+(of|in)?\s*([\w\s&]+)?"
        ]
        for line in self.text.split("\n"):
            for pat in patterns:
                match = re.search(pat, line, re.IGNORECASE)
                if match:
                    degree = match.group(1).lower().replace('.', '')
                    field = match.group(3).strip().lower() if match.group(3) else ""
                    education.append({"degree": degree, "field": field})
        return education
