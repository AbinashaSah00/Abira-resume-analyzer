# 🧠 Architecture Decision: CLI vs REST API for spaCy Container

As part of Abeera V1.0, we run `spaCy` inside a Docker container (`spacy_worker`) for skill extraction from Job Descriptions. There are two primary ways to integrate with this container from the main application: **CLI (subprocess)** or **REST API (FastAPI)**.

---

## 🔁 Option 1: CLI Integration (Current Approach)

We use Python's `subprocess.run()` to invoke a command in the container that takes in raw JD text and returns extracted skills.

### ✅ Pros
- ✅ Simple to implement
- ✅ Works well for single-user local tools
- ✅ No need to expose ports or run a server
- ✅ Easier to debug and control from main script

### ❌ Cons
- ❌ Harder to scale (no concurrent requests)
- ❌ Error handling is manual
- ❌ Limited observability/logging

---

## 🌐 Option 2: REST API Integration (Planned for Phase 2)

In this setup, we run a **FastAPI** server inside the container and send HTTP POST requests to `/extract_skills`. The server handles request parsing, skill extraction, and JSON responses.

### ✅ Pros
- ✅ Clean API interface for frontend/mobile/web
- ✅ Scalable — supports concurrent users
- ✅ Standardized response format (JSON)
- ✅ Easier to deploy as a service (Docker Compose, cloud)

### ❌ Cons
- ❌ More code: server, endpoints, validation
- ❌ Needs CORS, auth if public
- ❌ Slightly more setup time

---

## 📌 Current Setup (as of May 2025)

| Layer        | Approach Used       |
|--------------|---------------------|
| NLP Engine   | Docker container with spaCy |
| Integration  | CLI (subprocess call) from `main.py` |
| JD Processing | Skill extraction using skill DB |

---

## 🔄 Future Plan

| Phase        | Goal                     | Action                     |
|--------------|--------------------------|----------------------------|
| Phase 1      | Local Dev                | ✅ Use CLI                 |
| Phase 2      | Build Streamlit / Web UI | 🔄 Switch to REST (FastAPI) |
| Phase 3      | Deploy on Cloud          | 🔄 Use Docker Compose, REST |

---

## 📁 File Structure (In Future REST API Mode)

```bash
abeera_v1.0/
│
├── main.py
├── core/
│   └── matcher.py, resume_parser.py
├── spacy_worker/
│   ├── Dockerfile
│   ├── app.py       # FastAPI app
│   └── entrypoint.sh
├── data/
│   └── sample_resume.pdf
├── docs/
│   └── architecture_note.md
