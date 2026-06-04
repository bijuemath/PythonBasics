import os
from typing import TypedDict

from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt

from langgraph.checkpoint.sqlite import SqliteSaver




# --------------------------------------------------
# ENV
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# --------------------------------------------------
# STATE
# --------------------------------------------------

class LoanState(TypedDict):
    customer_name: str
    annual_income: float
    loan_amount: float

    risk_analysis: str
    risk_score: int

    manager_decision: bool

    final_status: str


# --------------------------------------------------
# NODE 1
# --------------------------------------------------

def analyze_risk(state: LoanState):
    print("\n========== RISK ANALYSIS ==========")

    prompt = f"""
You are a bank risk analyst.

Customer: {state['customer_name']}
Annual Income: {state['annual_income']}
Loan Amount: {state['loan_amount']}

Generate:

1. Risk analysis
2. Risk score from 1-100

Format:

RISK_SCORE: <number>

ANALYSIS:
<analysis>
"""

    response = llm.invoke(prompt)

    text = response.content

    score = 50

    try:

        for line in text.splitlines():

            if "RISK_SCORE" in line.upper():

                score = int(
                    ''.join(
                        c for c in line if c.isdigit()
                    )
                )

                break

    except Exception:
        score = 50

    response = llm.invoke(prompt)

    print(response.content)

    return {
        "risk_analysis": text,
        "risk_score": score
    }


# --------------------------------------------------
# NODE 2
# --------------------------------------------------

def manager_approval(state: LoanState):

    decision = interrupt(
        {
            "message":
            f"Approve loan for "
            f"{state['customer_name']} ?",

            "risk_score":
            state["risk_score"],

            "analysis":
            state["risk_analysis"]
        }
    )

    return {
        "manager_decision": bool(decision)
    }


# --------------------------------------------------
# ROUTER
# --------------------------------------------------

def approval_router(state: LoanState):

    if state["manager_decision"]:
        return "approve"

    return "reject"


# --------------------------------------------------
# APPROVE NODE
# --------------------------------------------------

def approve_loan(state: LoanState):

    return {
        "final_status":
        "APPROVED"
    }


# --------------------------------------------------
# REJECT NODE
# --------------------------------------------------

def reject_loan(state: LoanState):

    return {
        "final_status":
        "REJECTED"
    }


# --------------------------------------------------
# SQLITE CHECKPOINT
# --------------------------------------------------



with SqliteSaver.from_conn_string(
    "loan_checkpoints.db"
) as checkpointer:
    
    print(type(checkpointer))

# --------------------------------------------------
# GRAPH
# --------------------------------------------------

builder = StateGraph(LoanState)

builder.add_node("risk_analysis", analyze_risk)
builder.add_node("manager_review", manager_approval)
builder.add_node("approve", approve_loan)
builder.add_node("reject", reject_loan)

builder.set_entry_point("risk_analysis")

builder.add_edge(
    "risk_analysis",
    "manager_review"
)

builder.add_conditional_edges(
    "manager_review",
    approval_router,
    {
        "approve": "approve",
        "reject": "reject"
    }
)

builder.add_edge("approve", END)
builder.add_edge("reject", END)



graph = builder.compile(
        checkpointer=checkpointer
    )

# --------------------------------------------------
# EXECUTE
# --------------------------------------------------

THREAD_ID = "LOAN_1001"

config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}

with SqliteSaver.from_conn_string(
    "loan_checkpoints.db"
) as checkpointer:

    graph = builder.compile(
        checkpointer=checkpointer
    )

    result = graph.invoke(
        {
            "customer_name": "Biju Mathew",
            "annual_income": 800000,
            "loan_amount": 1500000,

            "risk_analysis": "",
            "risk_score": 0,

            "manager_decision": False,

            "final_status": ""
        },
        config=config
    )

    print("\n")
    print("=" * 80)
    print("WORKFLOW PAUSED")
    print("=" * 80)

    print("\nThread ID:", THREAD_ID)
    print("\nRun resume_workflow.py later.")