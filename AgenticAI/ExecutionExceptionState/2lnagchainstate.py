import os
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from dotenv import load_dotenv
import os
load_dotenv()
# 1. Initialize the Groq LLM
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

# Expanded Database with 5 Flight Items
FLIGHT_DB = {
    "AI101": {"status": "Delayed by 45 mins", "gate": "T3-12A", "destination": "Delhi"},
    "6E5322": {"status": "On Time", "gate": "T2-5", "destination": "Mumbai"},
    "UK945": {"status": "Boarding", "gate": "T3-8", "destination": "Bengaluru"},
    "AA230": {"status": "Cancelled due to weather", "gate": "N/A", "destination": "New York"},
    "EK506": {"status": "On Time", "gate": "Gate 21", "destination": "Dubai"}
}

# 2. Setup Manual Conversation Memory Store
memory_store: Dict[str, List[BaseMessage]] = {}

def get_chat_history(session_id: str) -> List[BaseMessage]:
    """Retrieves the message history array for a session."""
    if session_id not in memory_store:
        memory_store[session_id] = []
    return memory_store[session_id]

# 3. Create the Pure LangChain Core Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful airport customer service assistant. Speak kindly.\n\n"
               "Current Task State Details:\n{task_state_context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

core_chain = prompt | llm

# 4. Main Program Function (No changes made here)
def run_flight_assistant(user_message: str, session_id: str) -> str:
    """
    Manages task execution states and manual conversational memory 
    using warning-free pure LangChain components.
    """
    history = get_chat_history(session_id)
    
    execution_state: Dict[str, Any] = {
        "current_step": "parsing",
        "extracted_flight": None,
        "database_match": False,
        "flight_info": None
    }
    
    # --- Step 1: Handle State Logic (Extract Data) ---
    extraction_prompt = (
        f"Analyze this phrase: '{user_message}'. Extract any flight number mentioned. "
        "Respond ONLY with the flight code (e.g., AI101) or the word 'NONE'."
    )
    extracted_raw = llm.invoke(extraction_prompt).content.strip().upper()
    
    if "NONE" not in extracted_raw and len(extracted_raw) > 2:
        execution_state["extracted_flight"] = extracted_raw
        execution_state["current_step"] = "database_lookup"
        
        # --- Step 2: Handle State Logic (Database Check) ---
        flight_code = execution_state["extracted_flight"]
        if flight_code in FLIGHT_DB:
            execution_state["database_match"] = True
            execution_state["flight_info"] = FLIGHT_DB[flight_code]
            execution_state["current_step"] = "ready_to_respond"
        else:
            execution_state["current_step"] = "flight_not_found"
    else:
        execution_state["current_step"] = "general_conversation"

    # Format the step execution data for the prompt
    state_context_string = (
        f"- Current Workflow Step: {execution_state['current_step']}\n"
        f"- Found Flight Number: {execution_state['extracted_flight']}\n"
        f"- Verified DB Info: {execution_state['flight_info']}"
    )
    
    # --- Step 3: Run the Chain Natively ---
    response = core_chain.invoke({
        "user_input": user_message,
        "task_state_context": state_context_string,
        "chat_history": history
    })
    
    # --- Step 4: Manually Update Conversational Memory ---
    history.append(HumanMessage(content=user_message))
    history.append(AIMessage(content=response.content))
    
    return response.content

# 5. Interactive Runtime Loop
if __name__ == "__main__":
    session_thread = "passenger_terminal_session"
    print("====================================================")
    print("Airport Support Assistant Online (Type 'exit' to quit)")
    print("Available flights in system: AI101, 6E5322, UK945, AA230, EK506")
    print("====================================================\n")

    while True:
        user_msg = input("You: ")
        
        # Handle the break condition
        if user_msg.strip().lower() == "exit":
            print("Assistant: Thank you for stopping by. Have a safe flight!")
            break
            
        # Ignore empty entries
        if not user_msg.strip():
            continue
            
        # Run execution loop pipeline
        reply = run_flight_assistant(user_msg, session_id=session_thread)
        print(f"AI: {reply}\n")