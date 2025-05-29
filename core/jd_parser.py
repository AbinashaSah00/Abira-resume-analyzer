# core/jd_parser.py

import subprocess
import uuid
import json
import os

class JDParser:
    def __init__(self, jd_text: str):
        """
        Initialize the JDParser with raw job description text.
        """
        self.jd_text = jd_text
        self.extracted_skills = []

    def extract_skills(self, skills_db):
        """Calls spaCy skill extractor via Docker CLI."""
        import subprocess
        import uuid
        import json
        import os

        job_id = str(uuid.uuid4())[:8]
        input_file = f"input_{job_id}.txt"
        output_file = f"output_{job_id}.json"

        try:
            # Save JD text to file
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(self.jd_text)

            # Run spaCy extractor inside Docker
            subprocess.run([
                "docker", "exec", "spacy_worker", "python",
                "extract_skills.py", input_file, output_file
            ], check=True)

            # Copy file from container to host (optional if you write output to mounted volume)
            subprocess.run([
                "docker", "cp", f"spacy_worker:{output_file}", output_file
            ], check=True)

            # Load result
            with open(output_file, "r", encoding="utf-8") as f:
                result = json.load(f)

            # Cleanup
            os.remove(input_file)
            os.remove(output_file)

            return result.get("must_have", []), result.get("good_to_have", [])

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Docker execution failed: {e}")
        except Exception as e:
            print(f"[ERROR] JD parsing failed: {e}")

        return [], []
