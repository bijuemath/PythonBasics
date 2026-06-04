import os

from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter

from langgraph.graph import StateGraph, END

from state import AgentState
from tools import generate_sql
from db import execute_query, execute_update


load_dotenv()

llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)



def detect_intent(state):

    query = state["user_query"].lower()

    if any(keyword in query for keyword in ["change", "update", "set", "insert"]):
        state["intent"] = "UPDATE"
    else:
        state["intent"] = "SELECT"

    return state


def generate_select_sql(state):

    sql = generate_sql(
        state["user_query"],
        llm
    )

    state["sql_query"] = sql

    return state


def run_query(state):

    if state.get("intent") == "UPDATE":
        result = execute_update(
            state["sql_query"]
        )
    else:
        result = execute_query(
            state["sql_query"]
        )

    state["result"] = result

    return state


def format_response(state):

    state["response"] = str(
        state["result"]
    )

    return state


graph = StateGraph(AgentState)

graph.add_node(
    "intent",
    detect_intent
)

graph.add_node(
    "sql",
    generate_select_sql
)

graph.add_node(
    "execute",
    run_query
)

graph.add_node(
    "format",
    format_response
)

graph.set_entry_point("intent")

graph.add_edge(
    "intent",
    "sql"
)

graph.add_edge(
    "sql",
    "execute"
)

graph.add_edge(
    "execute",
    "format"
)

graph.add_edge(
    "format",
    END
)

agent = graph.compile()