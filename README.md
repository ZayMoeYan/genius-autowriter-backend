# Backend MVP - FastAPI + Gemini (placeholder) + Facebook Scheduler

This project is a minimal backend for the MVP you requested:
- Next.js frontend (separate) will call this backend.
- `POST /generate` will call Gemini (placeholder) to produce Myanmar content.
- `POST /schedule` will schedule a Facebook post using APScheduler.
- In-memory job store (APScheduler BackgroundScheduler) – suitable for MVP/testing.

**Important**
- Gemini integration is implemented as a placeholder function. Replace `ai.py` implementation with real Gemini API calls and credentials.
- Facebook posting uses the Meta Graph API endpoint (`/{page-id}/feed`). Provide a valid PAGE_ACCESS_TOKEN with `pages_manage_posts` permission.
- This project intentionally avoids databases for the MVP as requested. Jobs live in memory; restarting the process will lose scheduled jobs.

## How to run (development)
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill your variables if you want to test Facebook or Gemini.
3. Start the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. API docs: http://localhost:8000/docs

