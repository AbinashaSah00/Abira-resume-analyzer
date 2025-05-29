# core/semantic_matcher.py

from sentence_transformers import SentenceTransformer, util
import numpy as np
import re
from core.synonym_map import synonym_map  # ✅ Alias map


class SemanticSkillMatcher:
    def __init__(self, jd_skills, resume_skills, threshold=0.7):
        self.jd_skills = [s.lower() for s in jd_skills]
        self.resume_skills = [s.lower() for s in resume_skills]
        self.threshold = threshold
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def token_overlap_boost(self, a, b):
        a_tokens = set(re.findall(r"\w+", a))
        b_tokens = set(re.findall(r"\w+", b))
        common = a_tokens.intersection(b_tokens)
        if len(common) >= 1:
            return 0.05 + 0.05 * len(common)  # boost by 5–15%
        return 0

    def get_best_match(self, target_skill):
        target_skill = target_skill.lower()
        target_embedding = self.model.encode(target_skill, convert_to_tensor=True)
        resume_embeddings = self.model.encode(self.resume_skills, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(target_embedding, resume_embeddings)[0]

        best_score = similarities.max().item()
        best_index = int(np.argmax(similarities))
        best_match = self.resume_skills[best_index]

        # 🔁 Boost if token overlap is strong
        token_boost = self.token_overlap_boost(target_skill, best_match)

        # ✅ Boost if it's a known synonym
        synonym_boost = 0
        for key, aliases in synonym_map.items():
            if target_skill == key or target_skill in aliases:
                if best_match in aliases or best_match == key:
                    synonym_boost = 0.1
                    break

        boosted_score = min(1.0, best_score + token_boost + synonym_boost)

        # 📝 Explanation
        explanation = {
            "target": target_skill,
            "best_match": best_match,
            "original_score": round(best_score, 3),
            "token_boost": round(token_boost, 3),
            "synonym_boost": round(synonym_boost, 3),
            "final_score": round(boosted_score, 3)
        }

        if boosted_score >= self.threshold:
            return best_match, boosted_score, explanation
        else:
            return None, boosted_score, explanation

    def get_semantic_matches(self):
        matched = []
        partial = []
        unmatched = []

        for jd_skill in self.jd_skills:
            best_match, score, explanation = self.get_best_match(jd_skill)

            if score >= 0.85:
                matched.append((jd_skill, best_match, score, explanation))
            elif self.threshold <= score < 0.85:
                partial.append((jd_skill, best_match, score, explanation))
            else:
                unmatched.append((jd_skill, None, score, explanation))

        return {
            "matched": matched,
            "partial": partial,
            "unmatched": unmatched
        }
