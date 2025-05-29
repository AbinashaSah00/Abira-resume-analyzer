# ✨ AbiRa - Resume Analyzer
# Abeera V1.0 🤖 - The Smart JD-Resume CLI Matcher

**Abeera** (short for *AI-Based Resume Analyzer*) is a smart, local-first assistant designed to analyze your resume against any Job Description (JD) using lightweight LLMs, NLP pipelines, and a flexible scoring framework.

---

## 🚀 What is Abeera V1.0?

Abeera is a command-line tool that lets you:

* 📄 Upload your resume (PDF)
* � Paste any Job Description (JD)
* 🔍 Extract skills, titles, and education
* 🌍 Run a JD-Resume fit analysis using local LLMs
* ⭐ Get a skill gap summary and recommendations
* 🧠 Ask follow-up career questions in a local chat loop

All using **TinyLLaMA** model (1.1B chat GGUF version) on your system.

---

## 📊 Key Features

| Module                 | What it Does                                |
| ---------------------- | ------------------------------------------- |
| `main.py`              | CLI engine to run the full interaction      |
| `fast_skill_extractor` | LLM-powered comma-separated skill extractor |
| `title_extractor`      | LLM + regex-based title guesser             |
| `skill_gap_detector`   | Matched / Partial / Missing skill detection |
| `profile_scorecard`    | Heuristic scoring with LLM fallback parsing |
| `abeera_llm.py`        | TinyLLaMA CLI prompt wrapper                |
| `interaction_logger`   | Logs all prompts/responses to `outputs/`    |

---

## 🔧 How to Use (Quick Guide)

### Step 1: Clone + Install

```bash
$ git clone https://github.com/abinashsahoo/Abeera_V1.0.git
$ cd Abeera_V1.0
$ pip install -r requirements.txt
```

### Step 2: Download TinyLLaMA

Put your GGUF model in:

```
llm/bin/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

And llama-run.exe into:

```
llm/bin/llama-run.exe
```

### Step 3: Launch Abeera CLI

```bash
$ python main.py
```

It will ask you for:

1. 📄 Resume path (PDF)
2. � Paste JD (press Enter twice to finish)

---

## 🔎 What Abeera V1.0 Can and Can’t Do

### ✅ What Works Well

* Skill extraction from JD and resume
* Partial match logic (e.g. Tableau vs dashboard)
* Score breakdown (skills, tools, title, education)
* Resume feedback via follow-up prompts

### ❌ Current Limitations

* TinyLLaMA's reasoning is limited (6GB VRAM required)
* Resume parsing is regex/LLM based (not OCR/NER yet)
* Only works on GPU (Windows only due to llama-run.exe)
* Sometimes LLM returns incomplete or noisy JSON

---

## 🧪 The Tech Behind Abeera

| Layer       | Tools & Models                        |
| ----------- | ------------------------------------- |
| LLM backend | TinyLLaMA 1.1B Chat GGUF (local .exe) |
| Interface   | Python CLI (main.py)                  |
| NLP modules | Regex + LLM + Heuristic Scorecard     |
| Logging     | JSONL files in `outputs/` folder      |

---

## 💡 Future Vision (Abeera V2.0)

* [ ] Web UI with Streamlit / FastAPI
* [ ] Use OpenRouter or Mistral when available
* [ ] Resume section detection with spaCy
* [ ] Resume to job recommender
* [ ] Deployment as microservice with memory
* [ ] Explainability with SHAP-style highlights

---

## 📄 Sample Output Snapshot

```
🌐 JD Title: Sr Data Engineer
📄 Resume Title: Data Analyst
📉 Scorecard:
 - Skills Matched     : 16 / 40
 - Title Match        : 5 / 20
 - Experience         : 10 / 20
 - Education Match    : 10 / 10
 - Tools Match        : 2 / 10
 - Total Score        : 43 / 100
 - Fit Level          : MODERATE
```

```
📃 Skill Gap Summary:
✔️ Matched: sql, python
❌ Missing: azure, json
📈 Recommended Learning: learn azure, learn json, communication
```

---

## 💬 Contribute / Fork / Build Upon

This project is paused after V1.0 due to hardware limits (6GB VRAM).

You're welcome to:

* Fork and use a better LLM (like Mistral or GPT API)
* Add frontend (Streamlit)
* Improve PDF parsing with OCR/spaCy

---
Thanks for checking out Abeera V1.0 — let her help you one job at a time 🤖
---

## ✍️ Author

**Abinash Sahoo**  
*"Believe it until you make it."*
*"Building from rock bottom to relentless 🚀"*

- GitHub: [abinashsahoo00](https://github.com/abinashsahoo00)
- LinkedIn: [Abinash Sahoo](https://www.linkedin.com/in/abinash-sahoo/)
- Portfolio: [Abinash Sahoo](https://abinashasahoo-portfolio.netlify.app/)
with passion for career-tech ✨
