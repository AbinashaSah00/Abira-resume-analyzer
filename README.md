# ✨ AbiRa - Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.9-blue) 
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-ff69b4)

---

## 📖 Project Description

**AbiRa - Resume Analyzer** is a simple but powerful tool designed to analyze resumes against job descriptions.  
It extracts key information (like email, phone, skills) from resumes and matches them with job requirements to calculate a skill match score — helping candidates or recruiters quickly assess resume-job fit.

---

## 🗂️ Folder Structure

```
Resume_Analyzer/
│
├── core/
│   ├── analyzer.py
│   ├── extractor.py
│   ├── jd_parser.py
│   ├── matcher.py
│   ├── resume_parser.py
│   ├── tracker.py
│
├── data/
│   ├── Abinasha sahoo-Resume old.pdf
│   ├── Abinasha_Sahoo_Resume.pdf
│   ├── sample_jd.txt
│   ├── sample_resume.pdf
│
├── output/
│   ├── applications_log.csv
│   ├── resume_analysis_results.csv
│
├── utils/
│   └── text_utils.py
│
├── .gitignore
├── main.py
├── README.md
├── requirements.txt

```

---

## ⚙️ Features

- 📄 Extracts email and phone number from resumes.
- 🛠️ Cleans and preprocesses extracted resume text.
- 🔎 Extracts required skills from provided Job Description.
- 📊 Matches candidate's skills with JD skills and generates a skill match score.
- 🧠 Handles dynamic user input (resume path, JD text) at runtime.
- 📂 Saves result in CSV file for further use.

---

## 🛠️ Tech Stack

- **Python 3.9**
- **PyMuPDF** (`fitz`) for PDF text extraction
- **re** (Regular Expressions) for pattern matching
- **pandas** for data handling
- **VS Code** for development

---

## 🚀 Setup Instructions

1. **Clone the repository** (after pushing it on GitHub):

    ```bash
    git clone https://github.com/your-username/abira-resume-analyzer.git
    ```

2. **Navigate to the project folder**:

    ```bash
    cd abira-resume-analyzer
    ```

3. **Install required libraries**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the project**:

    ```bash
    python main.py
    ```

5. **Follow the prompts** to upload your resume and paste your job description!

---

## 🔮 Future Scope

- Upload multiple resumes and generate a ranking based on skill match score.
- Add basic machine learning for automatic skill extraction.
- Build a Streamlit web app for easier UI/UX.
- Integrate resume parsing with LinkedIn Job Postings.

---

## ✍️ Author

**Abinash Sahoo**  
*"Believe it until you make it."*
*"Building from rock bottom to relentless 🚀"*

- GitHub: [abinashsahoo00](https://github.com/abinashsahoo00)
- LinkedIn: [Abinash Sahoo](https://www.linkedin.com/in/abinash-sahoo/)
- LinkedIn: [Abinash Sahoo]([https://www.linkedin.com/in/abinash-sahoo/](https://www.notion.so/Hey-there-I-am-Abinash-Sahoo-1dfe544fcbea80ef973eec9fd705f513?pvs=4))
