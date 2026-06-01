from groq import Groq
from dotenv import load_dotenv
import os
import json
import random

# ----------------------------------
# LOAD ENV
# ----------------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------------
# AGENT STATE
# ----------------------------------

state = {
    "goal": "Find cheapest flight to Delhi",
    "sites_checked": [],
    "best_price": None,
    "best_site": None,
    "status": "running",
    "iterations": 0,
    "errors": 0
}

# ----------------------------------
# TOOLS
# ----------------------------------

def search_skyscanner():
    """Simulate API"""

    # Random failure
    if random.randint(1, 5) == 1:
        raise Exception("Skyscanner API Timeout")

    return {
        "site": "Skyscanner",
        "price": random.randint(5000, 8000)
    }


def search_makemytrip():

    if random.randint(1, 5) == 1:
        raise Exception("MakeMyTrip API Error")

    return {
        "site": "MakeMyTrip",
        "price": random.randint(5000, 8000)
    }


TOOLS = {
    "search_skyscanner": search_skyscanner,
    "search_makemytrip": search_makemytrip
}

# ----------------------------------
# EXECUTION LOOP
# ----------------------------------

MAX_ITERATIONS = 10

while True:

    print("\n==============================")
    print("CURRENT STATE")
    print(json.dumps(state, indent=2))
    print("==============================")

    # ----------------------------------
    # EXIT CONDITIONS
    # ----------------------------------

    if state["status"] == "completed":
        print("\nGOAL COMPLETED")
        break

    if state["iterations"] >= MAX_ITERATIONS:
        print("\nMAX ITERATIONS REACHED")
        break

    if state["errors"] >= 3:
        print("\nTOO MANY ERRORS")
        break

    # ----------------------------------
    # LLM REASONING
    # ----------------------------------

    prompt = f"""
You are a flight-search agent.

Current State:
{json.dumps(state, indent=2)}

Available Tools:
- search_skyscanner
- search_makemytrip

Rules:
1. Use each site only once.
2. Compare prices.
3. After checking both sites,
   return COMPLETE.
4. Return JSON only.

Examples:
{{"action":"search_skyscanner"}}
{{"action":"search_makemytrip"}}
{{"action":"COMPLETE"}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    llm_output = response.choices[0].message.content

    print("\nLLM THINKING")
    print(llm_output)

    # ----------------------------------
    # PARSE LLM RESPONSE
    # ----------------------------------

    try:

        action_json = json.loads(llm_output)

        action = action_json["action"]

    except Exception:

        print("Failed to parse LLM response")

        state["errors"] += 1
        continue

    # ----------------------------------
    # EXIT CONDITION
    # ----------------------------------

    if action == "COMPLETE":

        state["status"] = "completed"
        continue

    # ----------------------------------
    # TOOL EXECUTION
    # ----------------------------------

    try:

        print(f"\nEXECUTING TOOL: {action}")

        result = TOOLS[action]()

        print("TOOL RESULT:", result)

        state["sites_checked"].append(
            result["site"]
        )

        # Update best price

        if (
            state["best_price"] is None
            or
            result["price"] < state["best_price"]
        ):

            state["best_price"] = result["price"]

            state["best_site"] = result["site"]

    # ----------------------------------
    # ERROR HANDLING
    # ----------------------------------

    except Exception as e:

        print("\nTOOL FAILED")
        print(e)

        state["errors"] += 1

        continue

    # ----------------------------------
    # STATE UPDATE
    # ----------------------------------

    state["iterations"] += 1

    # ----------------------------------
    # AUTO COMPLETE
    # ----------------------------------

    if len(state["sites_checked"]) >= 2:

        state["status"] = "completed"

# ----------------------------------
# FINAL RESULT
# ----------------------------------

print("\nFINAL STATE")
print(json.dumps(state, indent=2))

print("\nCHEAPEST FLIGHT")

print(
    f"{state['best_site']} : ₹{state['best_price']}"
)