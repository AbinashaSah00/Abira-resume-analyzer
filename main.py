# main.py

import os
import csv
from datetime import datetime
from core.extractor import extract_text_from_pdf
from core.skill_extractor import extract_skills_from_jd
from core.matcher import calculate_match
from utils.text_utils import clean_text

# Define a set of common English stopwords to ignore while matching
stopwords = {'and', 'with', 'the', 'of', 'in', 'to', 'for', 'a', 'an', 'on', 'at', 'is', 'are', 'as'}

def load_text_from_file(file_path):
    """
    Load text from a PDF or text file.
    """
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ""

def get_user_inputs():
    """
    Ask the user for resume folder and JD input method.
    """
    resume_folder = input("Enter the folder path where your resumes are stored (folder only!): ").strip()

    # Check if resume folder is valid
    if not os.path.isdir(resume_folder):
        print("\n❌ Error: The path you entered is not a folder. Exiting.")
        exit()

    jd_choice = input("Do you want to (1) Paste a Job Description manually, or (2) Select a JD folder? Enter 1 or 2: ").strip()

    if jd_choice == '1':
        pasted_jd = input("\nPaste your Job Description text here (then press Enter):\n").strip()
        jd_texts = {"pasted_jd.txt": pasted_jd}
    elif jd_choice == '2':
        jd_folder = input("Enter the folder path where your job descriptions are stored: ").strip()
        if not os.path.isdir(jd_folder):
            print("\n❌ Error: The path you entered is not a folder. Exiting.")
            exit()

        jd_files = [f for f in os.listdir(jd_folder) if f.lower().endswith(('.pdf', '.txt'))]
        jd_texts = {}
        for jd_file in jd_files:
            jd_path = os.path.join(jd_folder, jd_file)
            jd_texts[jd_file] = load_text_from_file(jd_path)
    else:
        print("Invalid choice. Exiting.")
        exit()

    return resume_folder, jd_texts

def main():
    """
    Main driver function.
    """
    # Get folder paths and JD inputs
    resume_folder, jd_texts = get_user_inputs()

    # Collect all resume files
    resume_files = [f for f in os.listdir(resume_folder) if f.lower().endswith('.pdf')]

    # Handle if no resumes found
    if not resume_files:
        print("\n❌ No resumes found in the folder. Exiting.")
        exit()

    results = []

    # Process each resume and each JD
    for resume_file in resume_files:
        resume_path = os.path.join(resume_folder, resume_file)
        resume_text = clean_text(load_text_from_file(resume_path))

        for jd_name, jd_content in jd_texts.items():
            jd_content_clean = clean_text(jd_content)
            jd_skills = extract_skills_from_jd(jd_content_clean)

            # Remove common stopwords from skills
            jd_skills = [skill for skill in jd_skills if skill not in stopwords]

            match_percentage, matched_skills = calculate_match(resume_text, jd_skills)
            results.append([resume_file, jd_name, round(match_percentage, 2), ', '.join(matched_skills)])

    # Sort results by Match Percentage descending
    results = sorted(results, key=lambda x: x[2], reverse=True)

    # Create output folder if not exists
    os.makedirs('output', exist_ok=True)

    # Create output filename with current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"output/resume_analysis_results_{current_time}.csv"

    # Write results to CSV
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Resume Name', 'Job Description Name', 'Match Percentage', 'Matched Skills'])
        writer.writerows(results)

    print(f"\n[✔] Resume Matching Completed! Results saved at {output_path}")

if __name__ == "__main__":
    main()
