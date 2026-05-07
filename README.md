# AI Hospital Receptionist 🏥

A full‑stack AI‑powered virtual receptionist that allows patients to describe their symptoms in natural language. The system automatically classifies them into **General Ward**, **Emergency Ward**, or **Mental Health Ward**, collects their details (name, age, query) one step at a time, and saves the completed record to **Supabase**. Optionally, it can send a webhook notification to a hospital management tool like relay.app.

Built as part of the **IBM SkillsBuild AI Strategy & Business Intelligence Internship**.

---

## 🧰 Tech Stack

| Layer       | Technology               |
|-------------|--------------------------|
| **Frontend**| React (Vite) + Tailwind CSS |
| **Backend** | Python + FastAPI         |
| **AI Logic**| LangGraph (state machine)|
| **Database**| Supabase (PostgreSQL)    |
| **Webhook** | relay.app or any POST endpoint |

---

## 📁 Project Structure
ai-hospital-receptionist/
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── langgraph_flow.py
│ │ └── supabase_client.py
│ ├── requirements.txt
│ └── .env.example
├── frontend/
│ ├── src/
│ ├── package.json
│ ├── vite.config.js
│ └── tailwind.config.js
└── README.md

text

---

## 🚀 How to run the project on your machine

### 1. Prerequisites

Make sure you have these installed:

- **Node.js** (v18 or later) → [download](https://nodejs.org/)
- **Python** (3.9 or later) → [download](https://www.python.org/)
- **Git** → [download](https://git-scm.com/)
- A free **Supabase** account → [supabase.com](https://supabase.com)

### 2. Clone the repository

Open a terminal (Command Prompt, Git Bash, or any shell) and run:

```bash
git clone https://github.com/jigarmodh1248/ai-hospital-receptionist.git
cd ai-hospital-receptionist
3. Set up Supabase (only 3 steps)
Log in to Supabase and create a new project. Choose a name (any), a strong password (save it), and the region closest to you.

Once the project is created, go to Project Settings → API. Copy:

Project URL (e.g., https://xxxxx.supabase.co)

Legacy anon key (the long JWT starting with eyJ..., not the publishable key)

Run these SQL commands in the SQL Editor (copy all and click Run):

sql
CREATE TABLE IF NOT EXISTS patients (
    id serial PRIMARY KEY,
    patient_name text,
    patient_age text,
    patient_query text,
    ward text,
    timestamp timestamptz DEFAULT now()
);

GRANT USAGE ON SCHEMA public TO anon;
GRANT INSERT, SELECT ON public.patients TO anon;

ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anon insert" ON public.patients
FOR INSERT TO anon WITH CHECK (true);
4. Configure the backend
Inside the backend/ folder, create a file named .env with the following content:

text
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_anon_key_here
WEBHOOK_URL=
Replace the placeholders with the actual values from your Supabase project. Leave WEBHOOK_URL empty if you don’t have a webhook endpoint.

5. Install backend dependencies & start the server
bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload
The backend will run on http://localhost:8000.
You should see green logs and NO warning about Supabase credentials.

6. Install frontend dependencies & start the React app
Open a second terminal, still in the project root, then:

bash
cd frontend
npm install
npm run dev
The frontend will run on http://localhost:5173. Open that URL in your browser.

7. Test the application
The chat will greet you with: “Hello! I am your virtual receptionist. How can I help you today?”

Type a message describing your symptoms, for example:

I have a high fever and bad cough

I feel extremely anxious and can't sleep

I cut my hand and bleeding heavily

The assistant will ask for your name, age, and main query one by one.

Once all details are collected, a ward badge and a patient summary card will appear.

The patient record is saved to your Supabase patients table.

⚙️ How it works (technical summary)
React frontend sends each user message to the FastAPI /chat endpoint with a unique session_id.

FastAPI stores the conversation state (in‑memory for demo) and passes it through a LangGraph state machine.

LangGraph:

Router node classifies the symptom description into general_ward, emergency_ward, or mental_health_ward using keyword detection.

Clarification node checks which patient detail is missing (name, age, query) and asks for it politely, one at a time.

When all three fields are filled (collected = True), the backend:

Inserts a record into Supabase’s patients table.

Sends a JSON payload to the webhook URL (if configured).

The frontend updates to show the ward badge and summary card.

🛠️ Troubleshooting
Problem	Likely Solution
Backend shows Invalid API key	Make sure you used the legacy anon JWT key (starts with eyJ...), not the publishable key.
permission denied for table patients	Run the GRANT INSERT, SELECT ON public.patients TO anon; again in Supabase SQL Editor.
new row violates row-level security	Run the CREATE POLICY SQL command again.
Frontend can’t reach backend	Ensure the backend is running on http://localhost:8000 and you didn’t close its terminal.
Chat works but data not saved	Check the backend terminal for Supabase errors and ensure the SQL was executed correctly.
📜 License
This project was built for educational purposes as part of IBM SkillsBuild. Feel free to use and modify.

📧 Contact
Created by: MODH JIGAR AMITKUMAR
College: R. C. Technical Institute
Email: jigarmodh1248@gmail.com
