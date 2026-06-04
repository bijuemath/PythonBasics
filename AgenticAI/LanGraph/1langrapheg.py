from typing import TypedDict
from dotenv import load_dotenv
import traceback
import os

from langgraph.graph import StateGraph, END
from langchain_openrouter import ChatOpenRouter

# ==========================================================
# LOAD ENV
# ==========================================================

load_dotenv()

# ==========================================================
# LLM
# ==========================================================






llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,
    max_retries=2
)

# ==========================================================
# STATE
# ==========================================================

class AgentState(TypedDict):
    topic: str

    plan: str
    research: str
    review: str
    final_report: str

    approved: bool
    retry_count: int

    error: str


# ==========================================================
# SAFE LLM CALL
# ==========================================================

def ask_llm(prompt: str):

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as ex:
        print("LLM Error:", ex)
        raise


# ==========================================================
# PLANNER
# ==========================================================

def planner(state: AgentState):

    print("\n========== PLANNER ==========")

    prompt = f"""
You are a Planner Agent.

Topic:
{state["topic"]}

Create a detailed research plan.

Return:

1. Objectives
2. Key Topics
3. Research Steps
"""

    result = ask_llm(prompt)

    return {
        "plan": result
    }


# ==========================================================
# RESEARCHER
# ==========================================================

def researcher(state: AgentState):

    print("\n========== RESEARCHER ==========")

    previous_feedback = state.get("review", "")

    prompt = f"""
You are a Research Agent.

Topic:
{state["topic"]}

Plan:
{state["plan"]}

Reviewer Feedback:
{previous_feedback}

Create detailed research.

Minimum 400 words.
"""

    result = ask_llm(prompt)

    return {
        "research": result
    }


# ==========================================================
# REVIEWER
# ==========================================================

def reviewer(state: AgentState):

    print("\n========== REVIEWER ==========")

    prompt = f"""
You are a strict reviewer.

Research:

{state["research"]}

Rules:

Approve only if:
- Detailed
- Accurate
- Well structured
- More than 300 words

Respond EXACTLY:

APPROVED
Reason: ...

or

REJECTED
Reason: ...
"""

    result = ask_llm(prompt)

    approved = result.upper().startswith("APPROVED")

    return {
        "review": result,
        "approved": approved,
        "retry_count": state["retry_count"] + 1
    }


# ==========================================================
# WRITER
# ==========================================================

def writer(state: AgentState):

    print("\n========== WRITER ==========")

    prompt = f"""
You are a professional technical writer.

Topic:
{state["topic"]}

Research:
{state["research"]}

Create a polished final report.
"""

    result = ask_llm(prompt)

    return {
        "final_report": result
    }


# ==========================================================
# ERROR HANDLER
# ==========================================================

def error_node(state: AgentState):

    print("\n========== ERROR ==========")

    return {
        "final_report": f"""
Workflow failed.

Error:
{state['error']}
"""
    }


# ==========================================================
# ROUTER
# ==========================================================

MAX_RETRIES = 3

def review_router(state: AgentState):

    print(
        f"\nApproved={state['approved']} "
        f"Retry={state['retry_count']}"
    )

    if state["approved"]:
        return "writer"

    if state["retry_count"] >= MAX_RETRIES:
        print("Maximum retries reached.")
        return "writer"

    return "researcher"


# ==========================================================
# GRAPH
# ==========================================================

builder = StateGraph(AgentState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("reviewer", reviewer)
builder.add_node("writer", writer)
builder.add_node("error", error_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "reviewer")

builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "researcher": "researcher",
        "writer": "writer"
    }
)

builder.add_edge("writer", END)
builder.add_edge("error", END)

graph = builder.compile()

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    try:

        initial_state = {
            "topic": "Building Agentic AI Systems with LangGraph",

            "plan": "",
            "research": "",
            "review": "",
            "final_report": "",

            "approved": False,
            "retry_count": 0,

            "error": ""
        }

        result = graph.invoke(initial_state)

        print("\n")
        print("=" * 80)
        print("FINAL REPORT")
        print("=" * 80)
        print(result["final_report"])

    except Exception:

        traceback.print_exc()