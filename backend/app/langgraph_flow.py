from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END

# ================== State Definition ==================
class ConversationState(TypedDict):
    session_id: str
    messages: List[str]                # list of "user: ..." / "bot: ..."
    ward: str                          # one of "general_ward", "emergency_ward", "mental_health_ward"
    patient_name: Optional[str]
    patient_age: Optional[str]
    patient_query: Optional[str]
    collected: bool                    # True when all data gathered
    response: str                      # assistant's reply for this turn

# ================== Node Functions ==================
def router_node(state: ConversationState) -> ConversationState:
    """Classify ward based on latest user message if not already set."""
    if state.get("ward"):
        return state

    # get last user message
    last_msg = ""
    for msg in reversed(state["messages"]):
        if msg.startswith("user:"):
            last_msg = msg[5:].strip().lower()
            break

    # Simple keyword classification (can be replaced with LLM later)
    emergency_keywords = ["emergency", "accident", "bleeding", "chest pain", "unconscious", "severe", "heart attack", "stroke"]
    mental_keywords = ["depressed", "anxiety", "mental health", "suicidal", "stress", "overwhelmed", "counseling"]

    if any(word in last_msg for word in emergency_keywords):
        state["ward"] = "emergency_ward"
    elif any(word in last_msg for word in mental_keywords):
        state["ward"] = "mental_health_ward"
    else:
        state["ward"] = "general_ward"

    return state

def clarification_node(state: ConversationState) -> ConversationState:
    """Ask for missing patient details one at a time."""
    # If already collected, nothing to do
    if state.get("collected"):
        return state

    # Determine what's missing
    if not state.get("patient_name"):
        state["response"] = "To assist you better, may I know your full name?"
        return state
    if not state.get("patient_age"):
        state["response"] = f"Thank you, {state['patient_name']}. Could you please tell me your age?"
        return state
    if not state.get("patient_query"):
        state["response"] = "Thank you. Now, please describe your main health concern or query in a few words."
        return state

    # All collected
    state["collected"] = True
    state["response"] = "Thank you for providing your details. A nurse will be with you shortly."
    return state

def process_user_input(state: ConversationState, user_message: str) -> ConversationState:
    """Parse user's message to extract data if we are waiting for a specific field."""
    if state.get("collected"):
        # Already done, just respond politely
        state["response"] = "Your information has been recorded. Please wait for assistance."
        return state

    # Determine which field we are expecting
    if not state.get("patient_name"):
        # If name is missing, take the whole message as name
        state["patient_name"] = user_message.strip()
    elif not state.get("patient_age"):
        # take message as age
        state["patient_age"] = user_message.strip()
    elif not state.get("patient_query"):
        state["patient_query"] = user_message.strip()
    else:
        # All fields present, shouldn't reach here normally
        state["collected"] = True
        state["response"] = "Thank you. Your information is complete."

    # After extracting, we will let the graph continue to clarification_node to ask next question
    return state

# ================== Build LangGraph ==================
def create_flow():
    workflow = StateGraph(ConversationState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("clarification", clarification_node)

    # Edges: router -> clarification -> END
    workflow.set_entry_point("router")
    workflow.add_edge("router", "clarification")
    workflow.add_edge("clarification", END)

    return workflow.compile()

# This is used by main.py
graph = create_flow()

def run_conversation(state: dict) -> dict:
    """Run the graph for one invocation and return updated state."""
    result = graph.invoke(state)
    return result