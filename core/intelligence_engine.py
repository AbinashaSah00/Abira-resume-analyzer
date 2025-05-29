import pandas as pd
from difflib import SequenceMatcher
from pathlib import Path
from core.semantic_matcher import SemanticSkillMatcher

class SkillMatcher:
    def __init__(self, known_skills_path: str):
        with open(known_skills_path, 'r', encoding='utf-8') as f:
            self.known_skills = [skill.strip().lower() for skill in f.readlines()]

    def match_skills(self, input_text: str, threshold: float = 0.8) -> list:
        input_tokens = input_text.lower().split()
        matched_skills = set()

        for skill in self.known_skills:
            for word in input_tokens:
                similarity = SequenceMatcher(None, skill, word).ratio()
                if similarity >= threshold or skill in input_text:
                    matched_skills.add(skill)
        return list(matched_skills)


class SkillGapDetector:
    def __init__(self, jd_skills: list, resume_skills: list):
        self.jd_skills = jd_skills
        self.resume_skills = resume_skills

    def generate_gap_summary(self):
        matcher = SemanticSkillMatcher(jd_skills=self.jd_skills, resume_skills=self.resume_skills)
        semantic_results = matcher.get_semantic_matches()

        matched = semantic_results['matched']
        partial = semantic_results['partial']
        unmatched = semantic_results['unmatched']

        matched_skills = [item[0] for item in matched]
        partial_skills = [item[0] for item in partial]
        missing_skills = [item[0] for item in unmatched]

        recommended_gaps = list(set(missing_skills + partial_skills))

        return {
            "matched": matched,
            "partial": partial,
            "unmatched": unmatched,
            "recommended_gaps": recommended_gaps,
            "summary": {
                "total_requested": len(self.jd_skills),
                "fully_matched": len(matched),
                "partial_matches": len(partial),
                "missing": len(unmatched),
                "recommended_gaps": recommended_gaps
            }
        }


class LearningRecommender:
    def __init__(self, resource_csv_path: str):
        self.df = pd.read_csv(resource_csv_path)

    def recommend(self, missing_skills: list, prefer_free: bool = False) -> dict:
        recommendations = {}
        for skill in missing_skills:
            match = self.df[self.df['skill'].str.lower() == skill.lower()]
            if not match.empty:
                row = match.iloc[0]
                if pd.notna(row['platform']):
                    recommendations[skill] = {
                        "platform": row.get('platform', ''),
                        "title": row.get('title', ''),
                        "link": row.get('link', ''),
                        "duration_hrs": row.get('duration_hrs', ''),
                        "difficulty": row.get('difficulty', ''),
                        "source_type": row.get('source_type', ''),
                        "verified": row.get('verified', '')
                    }
                else:
                    recommendations[skill] = {
                        "platform": "Google Search",
                        "title": f"Learn {skill}",
                        "link": f"https://www.google.com/search?q=learn+{skill}",
                        "duration_hrs": '',
                        "difficulty": '',
                        "source_type": 'search',
                        "verified": False
                    }
            else:
                recommendations[skill] = {
                    "platform": "Google Search",
                    "title": f"Learn {skill}",
                    "link": f"https://www.google.com/search?q=learn+{skill}",
                    "duration_hrs": '',
                    "difficulty": '',
                    "source_type": 'search',
                    "verified": False
                }
        return recommendations



# 🔧 One-click Orchestration Function
def run_skill_analysis(jd_skills: list, resume_skills: list, learning_csv: str, threshold=0.75, prefer_free=False):
    print("🔍 Running skill gap detection engine...")

    gap_detector = SkillGapDetector(jd_skills, resume_skills, threshold=threshold)
    gap_results = gap_detector.generate_gap_summary()

    print("\n📌 Skill Gap Recommendations:", gap_results["recommended_gaps"])
    print("📊 Gap Summary:", gap_results["summary"])

    recommender = LearningRecommender(learning_csv)
    learning_paths = recommender.recommend(gap_results["recommended_gaps"], prefer_free=prefer_free)

    return {
        "semantic_matches": {
            "matched": gap_results["matched"],
            "partial": gap_results["partial"],
            "unmatched": gap_results["unmatched"]
        },
        "gap_summary": gap_results["summary"],
        "learning_resources": learning_paths
    }
