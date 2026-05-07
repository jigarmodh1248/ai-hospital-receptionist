import os
import uuid
import httpx
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .langgraph_flow import run_conversation, ConversationState
from .supabase_client import supabase

load_dotenv()

app = FastAPI(title="AI Hospital Receptionist")

# Allow frontend (localhost:5173) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (for demo purposes)
sessions = {}

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# Request/Response models
class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    response: str
    patient_name: str | None = None
    patient_age: str | None = None
    patient_query: str | None = None
    ward: str | None = None
    collected: bool = False

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # Get or create session state
    sid = req.session_id
    if sid not in sessions:
        sessions[sid] = ConversationState(
            session_id=sid,
            messages=[],
            ward="",
            patient_name=None,
            patient_age=None,
            patient_query=None,
            collected=False,
            response=""
        )

    state = sessions[sid]

    # Add user message to history
    state["messages"].append(f"user: {req.user_message}")

    # Process the message (extract data if waiting for a field)
    from .langgraph_flow import process_user_input  # local import to avoid circular
    state = process_user_input(state, req.user_message)

    # Run the LangGraph (router + clarification)
    updated_state = run_conversation(state)

    # Save back
    sessions[sid] = updated_state

    # If just completed, log to Supabase and trigger webhook
    if updated_state["collected"]:
        # Save to Supabase
        if supabase:
            try:
                data = {
                    "patient_name": updated_state["patient_name"],
                    "patient_age": updated_state["patient_age"],
                    "patient_query": updated_state["patient_query"],
                    "ward": updated_state["ward"],
                    "timestamp": datetime.utcnow().isoformat(),
                }
                supabase.table("patients").insert(data).execute()
            except Exception as e:
                print(f"Supabase insert error: {e}")

        # Trigger webhook
        if WEBHOOK_URL:
            payload = {
                "patient_name": updated_state["patient_name"],
                "patient_age": updated_state["patient_age"],
                "patient_query": updated_state["patient_query"],
                "ward": updated_state["ward"],
                "timestamp": datetime.utcnow().isoformat(),
            }
            async with httpx.AsyncClient() as client:
                try:
                    await client.post(WEBHOOK_URL, json=payload)
                except Exception as e:
                    print(f"Webhook delivery failed: {e}")

    return ChatResponse(
        response=updated_state["response"],
        patient_name=updated_state.get("patient_name"),
        patient_age=updated_state.get("patient_age"),
        patient_query=updated_state.get("patient_query"),
        ward=updated_state.get("ward"),
        collected=updated_state["collected"],
    )

@app.get("/")
def root():
    return {"message": "AI Hospital Receptionist Backend is running"}