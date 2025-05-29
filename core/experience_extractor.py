# core/experience_extractor.py

import re
from datetime import datetime
from dateutil import parser as date_parser
from collections import defaultdict

class ExperienceExtractor:
    def __init__(self, resume_text):
        self.text = resume_text
        self.experience_blocks = self._extract_experience_blocks()

    def _extract_experience_blocks(self):
        """
        Extract potential job sections using keywords.
        """
        lines = self.text.split('\n')
        job_titles = ["data analyst", "business analyst", "software engineer", "intern", "consultant",
                      "developer", "manager", "scientist", "associate", "lead"]

        blocks = []
        current_block = []

        for line in lines:
            lower_line = line.lower()
            if any(title in lower_line for title in job_titles):
                if current_block:
                    blocks.append(" ".join(current_block))
                    current_block = []
            current_block.append(line.strip())

        if current_block:
            blocks.append(" ".join(current_block))

        return blocks

    def _extract_dates(self, text):
        """Extract start and end dates from a text block."""
        date_patterns = [
            r'(\w+ \d{4})\s*[\u2013\-to]+\s*(\w+ \d{4}|present)',
            r'(\d{2}/\d{4})\s*[\u2013\-to]+\s*(\d{2}/\d{4}|present)',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    start = date_parser.parse(match.group(1))
                    end = datetime.now() if 'present' in match.group(2).lower() else date_parser.parse(match.group(2))
                    return (start, end)
                except:
                    continue
        return None

    def parse_experience(self):
        """Returns list of experience with title, company, and duration in months."""
        experiences = []

        for block in self.experience_blocks:
            date_range = self._extract_dates(block)
            if not date_range:
                continue

            duration_months = (date_range[1].year - date_range[0].year) * 12 + (date_range[1].month - date_range[0].month)

            # Try to extract title and company heuristically
            title_match = re.search(r'(?i)(data analyst|business analyst|software engineer|consultant|manager|intern|scientist|developer)', block)
            title = title_match.group(1) if title_match else "Unknown"

            company_match = re.search(r'at\s+([A-Za-z0-9 &]+)', block)
            company = company_match.group(1).strip() if company_match else "Unknown"

            experiences.append({
                "title": title.title(),
                "company": company,
                "duration_months": duration_months,
                "from": date_range[0].strftime('%b %Y'),
                "to": date_range[1].strftime('%b %Y') if date_range[1] != datetime.now() else "Present"
            })

        return experiences

    def total_experience_months(self):
        parsed = self.parse_experience()
        return sum([x["duration_months"] for x in parsed])

    def total_experience_years(self):
        return round(self.total_experience_months() / 12.0, 2)
