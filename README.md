# AI Hospital Receptionist

A full‑stack AI‑powered hospital receptionist system that:
- Accepts natural language input from patients
- Classifies them into General, Emergency, or Mental Health wards
- Collects name, age, and query step‑by‑step
- Saves data to Supabase and triggers a webhook

**Tech Stack**
- Frontend: React (Vite) + Tailwind CSS
- Backend: Python + FastAPI
- AI Flow: LangGraph
- Database: Supabase

## How to Run (Locally)

### Backend
1. cd backend
2. python -m venv venv
3. venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
4. pip install -r requirements.txt
5. Copy .env.example to .env and fill SUPABASE_URL, SUPABASE_KEY
6. uvicorn app.main:app --reload

### Frontend
1. cd frontend
2. npm install
3. npm run dev

Open http://localhost:5173

## Supabase Setup
Run the SQL provided in `supabase_setup.sql` to create the patients table and policies.

## Demo
[Optional: Add a screenshot or GIF]