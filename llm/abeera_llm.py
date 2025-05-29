##llm/abeera_llm.py

import subprocess
from pathlib import Path

def ask_llama_local(prompt: str, model_path: str = "llm/bin/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf") -> str:
    """
    Calls local TinyLLaMA from project directory using a strict prompt structure.
    """
    llama_bin = Path("llm/bin/llama-run.exe")

    # Stronger prompt formatting to force short, clean output
    instruction = f"""
You are a resume and job description analyzer.
Your task is to respond to the following query **only** with the requested output format.
Avoid any explanations, markdown formatting, headings, or sentences.
If asked to list items, give a comma-separated flat list. No numbering. No paragraphs.

QUERY:
{prompt}
""".strip()

    try:
        result = subprocess.run(
            [str(llama_bin), model_path, instruction],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(Path.cwd()),
            timeout=180
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"[LLAMA ERROR] {e}"
