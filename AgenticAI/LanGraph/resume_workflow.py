from typing import TypedDict

from dotenv import load_dotenv
import os

from langchain_openrouter import ChatOpenRouter

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command

from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


class LoanState(TypedDict):
    customer_name: str
    annual_income: float
    loan_amount: float

    risk_analysis: str
    risk_score: int

    manager_decision: bool

    final_status: str


def analyze_risk(state):
    return {}


def manager_approval(state):

    decision = interrupt(
        {
            "message": "Manager approval"
        }
    )

    return {
        "manager_decision": bool(decision)
    }


def approval_router(state):

    if state["manager_decision"]:
        return "approve"

    return "reject"


def approve_loan(state):

    return {
        "final_status": "APPROVED"
    }


def reject_loan(state):

    return {
        "final_status": "REJECTED"
    }



with SqliteSaver.from_conn_string(
    "loan_checkpoints.db"
) as checkpointer:


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

THREAD_ID = "LOAN_1001"

config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}

decision = input(
    "Approve Loan? (yes/no): "
)

approve = (
    decision.lower().strip() == "yes"
)

with SqliteSaver.from_conn_string(
    "loan_checkpoints.db"
) as checkpointer:

    graph = builder.compile(
        checkpointer=checkpointer
    )

    result = graph.invoke(
        Command(resume=approve),
        config=config
    )

    print("\n")
    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)
    print(result)