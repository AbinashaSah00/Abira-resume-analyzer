# 📄 Resume Analyzer (AbiRa)

A smart and dynamic Resume Analyzer that matches multiple resumes against multiple job descriptions using real-time skill extraction and dynamic matching.  
Built with love as part of AbiRa — my AI journey! 🚀

---

## 🚀 Features

- 📂 Upload multiple resumes (.pdf)
- 📝 Paste job descriptions manually OR upload multiple JDs (.txt / .pdf)
- 🔎 Dynamic keyword extraction (NLP-based)
- 🧹 Stopwords cleaning for smarter matching
- 📊 Auto-calculates match percentages
- 📈 Results sorted by top matches
- 🗂️ Clean CSV output with match % and matched skills
- ⏱️ Timestamps on output files
- ❌ Friendly error handling (wrong paths / missing files)

---

## 🛠️ Tech Stack

- Python
- PyMuPDF (PDF parsing)
- Regular Expressions (skill extraction)
- CSV module (output generation)
- Clean modular codebase

---

## 📦 Installation

```bash
git clone https://github.com/AbinashaSah00/Abira-resume-analyzer.git
cd Abira-resume-analyzer
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python main.py
```
- Enter resume folder path when asked.
- Choose to paste a JD manually OR select a JD folder.
- Get clean CSV output inside the `/output/` folder!

---

## 📊 Output Example

| Resume Name | Job Description | Match % | Skills Matched |
|:------------|:----------------|:--------|:---------------|
| resume_data_analyst.pdf | jd_data_analyst.txt | 40% | python, sql, data, analyst, power |

_(Output file auto-generated with date and time stamp.)_

---

## 🎯 Future Work (Planned)

- Add small Streamlit front-end for drag-drop UI
- Integrate live job search APIs (Indeed, LinkedIn)
- OCR handling for scanned resumes
- Email notifications of best matches

---

## 🧑‍💻 Author

- Abinash Sahoo
- GitHub: [abinashsahoo00](https://github.com/abinashsahoo00)
- LinkedIn: [Abinash Sahoo](https://www.linkedin.com/in/abinash-sahoo/)
- Notion: [Abinash Sahoo](https://www.notion.so/Hey-there-I-am-Abinash-Sahoo-1dfe544fcbea80ef973eec9fd705f513?pvs=4)

---

**Believe it until you make it.** 🚀
```
