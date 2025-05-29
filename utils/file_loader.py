# utils/file_loader.py

def load_skills_db(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Skill DB not found at: {file_path}")
        return []
