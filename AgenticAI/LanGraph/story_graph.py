from typing import TypedDict
import os   

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.8
)



class StoryState(TypedDict):
    characters: str
    environment: str

    current_step: int
    max_steps: int

    last_choice: str

    story_text: str

    option1: str
    option2: str


def generate_story(state: StoryState):

    is_final = (
        state["current_step"] >= state["max_steps"]
    )

    if is_final:

        prompt = f"""
Continue and FINISH the story.

Characters:
{state['characters']}

Environment:
{state['environment']}

Story so far:
{state['story_text']}

Last Choice:
{state['last_choice']}

Write ONLY one final ending paragraph.
"""

        ending = llm.invoke(prompt).content

        return {
            "story_text":
            state["story_text"] + "\n\n" + ending,

            "option1": "",
            "option2": ""
        }

    prompt = f"""
You are creating an interactive story.

Characters:
{state['characters']}

Environment:
{state['environment']}

Story So Far:
{state['story_text']}

Last Choice:
{state['last_choice']}

Write:

PARAGRAPH:
(one paragraph)

OPTION1:
(short choice)

OPTION2:
(short choice)
"""

    response = llm.invoke(prompt).content

    print("\n========== GPT RESPONSE ==========")
    print(response)
    print("==================================")
    state["story_text"] = response
    paragraph = ""
    option1 = ""
    option2 = ""

    for line in response.splitlines():

        line = line.strip()

        if line.startswith("PARAGRAPH:"):
            paragraph = line.replace(
                "PARAGRAPH:",
                ""
            ).strip()

        elif line.startswith("OPTION1:"):
            option1 = line.replace(
                "OPTION1:",
                ""
            ).strip()

        elif line.startswith("OPTION2:"):
            option2 = line.replace(
                "OPTION2:",
                ""
            ).strip()

    story = state["story_text"]

    if story:
        story += "\n\n"

    story += paragraph

    return {
        "story_text": story,
        "option1": option1,
        "option2": option2
    }


builder = StateGraph(StoryState)

builder.add_node(
    "generate_story",
    generate_story
)

builder.set_entry_point(
    "generate_story"
)

builder.add_edge(
    "generate_story",
    END
)

graph = builder.compile()