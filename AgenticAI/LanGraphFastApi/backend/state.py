from typing import TypedDict

class AgentState(TypedDict):

    user_query: str

    intent: str

    sql_query: str

    result: list

    confirmation_needed: bool

    pending_action: dict

    response: str