# main.py

import os
import csv
from core.resume_parser import extract_resume_text
from utils.text_utils import clean_text
from core.extractor import extract_email, extract_phone, extract_skills
from colorama import Fore, Style, init

init(autoreset=True)

# 📍 Set CSV save location
csv_file = r"D:\Data Science\AbiRa\Resume Analyzer\output\resume_analysis_results.csv"

# Step 1: Ask user for resume file
print(Fore.CYAN + "📄 Please provide your resume path (or press Enter to select from available PDFs):")
resume_path = input("Resume Path: ").strip()

# If user leaves input empty, list PDFs to select
if not resume_path:
    pdf_dir = r"D:\Data Science\AbiRa\Resume Analyzer\data"
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(Fore.RED + "🚫 No PDF files found in 'data' folder. Please add a resume.")
        exit()

    print(Fore.YELLOW + "\nAvailable PDFs:")
    for idx, pdf in enumerate(pdf_files, start=1):
        print(f"{idx}. {pdf}")
    
    choice = int(input("\nEnter the number of the resume you want to select: "))
    resume_path = os.path.join(pdf_dir, pdf_files[choice - 1])

# Verify file exists
if not os.path.isfile(resume_path):
    print(Fore.RED + f"🚫 Resume file not found: {resume_path}")
    exit()

# Step 2: Ask user for JD text
jd_text = input("\n📝 Paste the Job Description text: ").strip()

# Step 3: Extract and clean resume text
raw_text = extract_resume_text(resume_path)
cleaned_text = clean_text(raw_text)

# Step 4: Extract Email and Phone from Resume
email = extract_email(raw_text)
phone = extract_phone(raw_text)

# Step 5: Extract Required Skills from JD
skills_database = [
    "Python", "SQL", "Excel", "Power BI", "Tableau",
    "Machine Learning", "Deep Learning", "Data Analysis", "Data Visualization",
    "Natural Language Processing", "NLP", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
    "Statistics", "Probability", "A/B Testing", "Hypothesis Testing",
    "Business Intelligence", "ETL", "Data Warehousing", "Big Data",
    "AWS", "Azure", "GCP", "Snowflake", "Databricks", "Apache Spark",
    "Data Cleaning", "Data Wrangling", "Regression", "Classification",
    "Clustering", "Time Series Analysis", "Dashboards", "SQL Queries", "Stored Procedures",
    "Microsoft Excel", "Advanced Excel", "VLOOKUP", "Pivot Tables", "Power Query",
    "Data Modeling", "Google Analytics", "Looker Studio", "Alteryx",
    "Data Mining", "Data Engineering Basics"
]

required_skills = extract_skills(jd_text, skills_database)
matched_skills = [skill for skill in required_skills if skill.lower() in cleaned_text.lower()]

# Step 6: Skill Match Score
if required_skills:
    match_score = round(len(matched_skills) / len(required_skills) * 100, 2)
else:
    match_score = 0.0

# Step 7: Show Results
print(Fore.GREEN + "\n📋 Resume Analysis Result:")
print(f"Extracted Email: {email}")
print(f"Extracted Phone: {phone}")
print(f"Required Skills from JD: {required_skills}")
print(f"Matched Skills: {matched_skills}")
print(f"Skill Match Score: {match_score}%")

# Step 8: Save the output to CSV
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        # write headers first if file doesn't exist
        writer.writerow(["Email", "Phone", "Required Skills", "Matched Skills", "Match Score"])

    writer.writerow([email, phone, ", ".join(required_skills), ", ".join(matched_skills), match_score])

print(Fore.CYAN + f"\n✅ Analysis result saved to {csv_file}")
