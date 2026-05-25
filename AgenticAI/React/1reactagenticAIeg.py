from groq import Groq
from dotenv import load_dotenv
import os
import re

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# TOOLS
# =========================

def calculator_tool(question):

    expression = re.sub(
        r"[^0-9+\-*/().]",
        "",
        question
    )

    result = eval(expression)

    return result


def weather_tool(city):

    weather_data = {
        "chennai": "35°C Sunny",
        "delhi": "30°C Hot"
    }

    return weather_data.get(
        city.lower(),
        "Weather not found"
    )

# =========================
# AGENT
# =========================

def react_agent(question):

    print("\n========================")
    print("USER QUESTION:")
    print(question)

    # =====================
    # REASON (THOUGHT)
    # =====================

    prompt = f"""
You are a REACT AI agent.

Available tools:
1. calculator
2. weather

Question:
{question}

Think carefully.

Which tool should you use?

Return ONLY:
calculator
weather
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    tool_name = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # =====================
    # THOUGHT
    # =====================

    print("\nTHOUGHT:")
    print(f"I should use {tool_name} tool.")

    # =====================
    # ACTION
    # =====================

    print("\nACTION:")

    if tool_name == "calculator":

        print("Calling calculator tool...")

        observation = calculator_tool(
            question
        )

    elif tool_name == "weather":

        print("Calling weather tool...")

        city = "Chennai"

        if "delhi" in question.lower():
            city = "Delhi"

        observation = weather_tool(city)

    else:

        observation = "Unknown tool"

    # =====================
    # OBSERVATION
    # =====================

    print("\nOBSERVATION:")
    print(observation)

    # =====================
    # FINAL ANSWER
    # =====================

    final_prompt = f"""
Question:
{question}

Observation:
{observation}

Generate final answer.
"""

    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0.3
    )

    final_answer = (
        final_response
        .choices[0]
        .message
        .content
    )

    print("\nFINAL ANSWER:")
    print(final_answer)

    print("========================\n")

# =========================
# MAIN LOOP
# =========================

while True:

    question = input(
        "Ask Question (exit to quit): "
    )

    if question.lower() == "exit":
        break

    react_agent(question)