from groq import Groq
from dotenv import load_dotenv
import os
import re

# =========================
# LOAD ENV
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

def agent(question):

    print("\nUSER QUESTION:")
    print(question)

    # =====================
    # LLM DECIDES TOOL
    # =====================

    prompt = f"""
You are an AI agent.

Available tools:
1. calculator
2. weather

Question:
{question}

Choose the best tool.

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

    print("\nLLM THOUGHT:")
    print(f"I should use: {tool_name}")

    # =====================
    # EXECUTE TOOL
    # =====================

    if tool_name == "calculator":

        result = calculator_tool(question)

    elif tool_name == "weather":

        city = "Chennai"

        if "delhi" in question.lower():
            city = "Delhi"

        result = weather_tool(city)

    else:

        result = "Unknown tool"

    # =====================
    # FINAL OUTPUT
    # =====================

    print("\nTOOL OUTPUT:")
    print(result)

# =========================
# MAIN LOOP
# =========================

while True:

    question = input(
        "\nAsk Question (exit to quit): "
    )

    if question.lower() == "exit":
        break

    agent(question)