#llm/abeera_agent.py

from llm.abeera_llm import ask_llama_local
from llm.interaction_logger import log_interaction

def analyze_gap_with_llm(jd_text: str, resume_text: str, purpose: str = "gap") -> str:
    """
    Sends JD and resume to local LLM to perform a human-like analysis.
    Purpose can be 'gap', 'rewrite', or 'interview_prep'
    """
    if purpose == "gap":
        prompt = f"""You are a smart career assistant. Read the job description and resume below.

Job Description:
{jd_text}

Resume:
{resume_text}

Now tell me:
- Which skills are missing in this resume?
- Which are partially aligned?
- Which are fully matched?

Respond in structured format under headings: Fully Matched, Partially Matched, and Missing Skills."""
    
    elif purpose == "rewrite":
        prompt = f"""Rewrite the following resume to better align with this job description.

Job Description:
{jd_text}

Resume:
{resume_text}

Make it concise, ATS-friendly, and highlight key skills."""
    
    elif purpose == "interview_prep":
        prompt = f"""Pretend you are a hiring manager. Based on the following job and resume, ask 3 technical questions and 2 behavioral questions.

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    else:
        return "[ERROR] Unknown purpose given."

    response = ask_llama_local(prompt)
    log_interaction(prompt, response)
    return response
