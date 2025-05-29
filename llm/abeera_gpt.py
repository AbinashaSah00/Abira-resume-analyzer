##llm/abeera_gpt.py
 
import json
from pathlib import Path

OUTPUT_DIR = Path("outputs")
LOG_PATH = OUTPUT_DIR / "interactions.jsonl"
TRAINING_PATH = OUTPUT_DIR / "training_data.txt"

def preprocess_logs_for_training():
    """Creates a text file of prompt-response pairs for AbeeraGPT training."""
    if not LOG_PATH.exists():
        print("[⚠️] No interactions.jsonl found. Nothing to preprocess.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with LOG_PATH.open("r", encoding="utf-8") as infile, \
         TRAINING_PATH.open("w", encoding="utf-8") as outfile:

        for line in infile:
            try:
                record = json.loads(line)
                prompt = record.get("prompt", "").strip()
                response = record.get("response", "").strip()
                outfile.write(f"{prompt}\n{response}\n\n")
            except json.JSONDecodeError:
                print("[⚠️] Skipping bad log line.")

    print(f"[✅] Preprocessed training data saved to {TRAINING_PATH}")
