# main.py


import os
import time
import sys
from pathlib import Path

from core.title_extractor import TitleExtractor
from core.fast_skill_extractor import FastSkillExtractor
from core.skill_gap_detector import SkillGapDetector
from core.profile_scorecard import compute_profile_score
from llm.abeera_llm import ask_llama_local

from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def classify_fit(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"

def main():
    print("\n🚀 Welcome to Abeera CLI - Smart JD & Resume Analyzer")

    # Step 1: Load Resume
    resume_path = input("📁 Enter path to your resume PDF: ").strip()
    if not Path(resume_path).exists():
        print("❌ Resume file not found!")
        sys.exit(1)
    resume_text = extract_text_from_pdf(resume_path)

    # Step 2: Paste JD
    print("\n📝 Paste the Job Description (JD) below. Press ENTER twice to finish:\n")
    jd_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        jd_lines.append(line)
    jd_text = "\n".join(jd_lines)

    # Step 3: Extract Titles and Skills
    title_extractor = TitleExtractor()
    skill_extractor = FastSkillExtractor()

    jd_title, _, _ = title_extractor.extract(jd_text, source="jd")
    resume_title, _, _ = title_extractor.extract(resume_text, source="resume")
    jd_skills = skill_extractor.extract_skills(jd_text, source="jd")
    resume_skills = skill_extractor.extract_skills(resume_text, source="resume")

    print(f"\n📌 JD Title: {jd_title}")
    print(f"📄 Resume Title: {resume_title}")
    print(f"🛠️ JD Skills: {jd_skills}")
    print(f"🧠 Resume Skills: {resume_skills}")

    # Step 4: Skill Gap Detection
    gapper = SkillGapDetector(jd_skills, resume_skills)
    gap_summary = gapper.gap_summary()

    print("\n📊 Skill Gap Summary")
    print(f"✅ Matched: {len(gap_summary['fully_matched'])}")
    print(f"🤝 Partial Matches: {len(gap_summary['partial_matches'])}")
    print(f"❌ Missing: {len(gap_summary['missing'])}")
    print(f"📌 Recommended Gaps: {gap_summary['recommended_gaps']}")

    # Step 5: Suggest Learning
    print("\n📚 Suggested Learning Paths:")
    for skill in gap_summary['recommended_gaps']:
        url = f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}"
        print(f"🔹 {skill.title()} → Google Search | Learn {skill} | {url}")

    # Step 6: Scorecard
    scorecard = compute_profile_score(
        jd_titles=[jd_title],
        resume_titles=[resume_title],
        jd_skills=jd_skills,
        resume_skills=resume_skills,
        experience_years=1.5,  # Placeholder, could be extracted later
        jd_degrees=["b.tech"],  # Placeholder
        resume_degrees=["bba"]  # Placeholder
    )

    scores = scorecard.get("scores", {})
    fit = classify_fit(scores.get("total", 0))

    print("\n📋 Profile Match Scorecard")
    print(f"🎯 Skill Match         : {scores.get('skills', 0)} / 40")
    print(f"👤 Title Match         : {scores.get('title_match', 0)} / 20")
    print(f"⏳ Experience Duration : {scores.get('experience_duration', 0)} / 20")
    print(f"🛠️ Tool Match          : {scores.get('tools', 0)} / 10")
    print(f"🎓 Education Match     : {scores.get('education_match', 0)} / 10")
    print(f"✅ Total Profile Score : {scores.get('total', 0)} / 100")
    print(f"\n📌 Fit Level: {fit}")

    # Step 7: Chat mode
    print("\n🤖 Abeera is ready for your questions (type 'bye bye' to exit):")
    while True:
        user_input = input("\n🗣️ You: ").strip()
        if user_input.lower() == "bye bye":
            print("👋 Goodbye!")
            break
        if not user_input:
            continue

        ai_response = ask_llama_local(user_input)
        print(f"🤖 Abeera: {ai_response}")

if __name__ == "__main__":
    main()

