##llm/interaction_logger.py

import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("outputs")
LOG_PATH = OUTPUT_DIR / "interactions.jsonl"

def log_interaction(prompt: str, response: str, model: str = "tinyllama"):
    """Logs each prompt-response pair to interactions.jsonl in the outputs folder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "prompt": prompt,
        "response": response
    }

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
