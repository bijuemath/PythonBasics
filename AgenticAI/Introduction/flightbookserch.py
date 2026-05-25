from groq import Groq
from dotenv import load_dotenv
import json
import os

# -----------------------------------
# LOAD ENV
# -----------------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------------
# MOCK FLIGHT SEARCH TOOLS
# -----------------------------------

def search_skyscanner(destination, date):

    print("\n[TOOL] Searching Skyscanner...")

    return {
        "website": "Skyscanner",
        "price": 8500,
        "airline": "IndiGo"
    }


def search_makemytrip(destination, date):

    print("\n[TOOL] Searching MakeMyTrip...")

    return {
        "website": "MakeMyTrip",
        "price": 9200,
        "airline": "Air India"
    }


def search_yatra(destination, date):

    print("\n[TOOL] Searching Yatra...")

    return {
        "website": "Yatra",
        "price": 8100,
        "airline": "Vistara"
    }


# -----------------------------------
# AVAILABLE TOOLS
# -----------------------------------

tools = [

    {
        "type": "function",
        "function": {
            "name": "search_skyscanner",
            "description": "Search flights on Skyscanner",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    }
                },
                "required": ["destination", "date"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_makemytrip",
            "description": "Search flights on MakeMyTrip",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    }
                },
                "required": ["destination", "date"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_yatra",
            "description": "Search flights on Yatra",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    }
                },
                "required": ["destination", "date"]
            }
        }
    }
]


# -----------------------------------
# USER QUESTION
# -----------------------------------

user_question = "Book the cheapest flight to Delhi next Friday"


# -----------------------------------
# SYSTEM PROMPT
# -----------------------------------

system_prompt = """
You are an intelligent travel agent.

Your job:
1. Understand the request
2. Think step-by-step
3. Search multiple websites
4. Compare prices
5. Find the cheapest flight
6. Explain your reasoning

Always think before calling tools.
"""


# -----------------------------------
# FIRST LLM CALL
# -----------------------------------

print("\n========== AGENT START ==========")

response = client.chat.completions.create(

    model="llama-3.3-70b-versatile",

    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_question
        }
    ],

    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message


# -----------------------------------
# TOOL EXECUTION
# -----------------------------------

tool_results = []

if message.tool_calls:

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(tool_call.function.arguments)

        print("\n================================")
        print("[AGENT THINKING]")
        print(f"I should use: {tool_name}")
        print("Arguments:", arguments)

        # -----------------------------------
        # EXECUTE TOOL
        # -----------------------------------

        if tool_name == "search_skyscanner":

            result = search_skyscanner(
                arguments["destination"],
                arguments["date"]
            )

        elif tool_name == "search_makemytrip":

            result = search_makemytrip(
                arguments["destination"],
                arguments["date"]
            )

        elif tool_name == "search_yatra":

            result = search_yatra(
                arguments["destination"],
                arguments["date"]
            )

        else:
            result = {"error": "Unknown tool"}

        print("\n[OBSERVATION]")
        print(result)

        tool_results.append(result)


# -----------------------------------
# FIND CHEAPEST FLIGHT
# -----------------------------------

cheapest = min(tool_results, key=lambda x: x["price"])

print("\n================================")
print("[AGENT DECISION]")

print(
    f"Cheapest flight found on "
    f"{cheapest['website']}"
)

print(
    f"Price: ₹{cheapest['price']}"
)

# -----------------------------------
# FINAL RESPONSE
# -----------------------------------

final_prompt = f"""
User Request:
{user_question}

Search Results:
{tool_results}

Cheapest Flight:
{cheapest}

Generate final response.
"""

final_response = client.chat.completions.create(

    model="llama-3.3-70b-versatile",

    messages=[
        {
            "role": "user",
            "content": final_prompt
        }
    ]
)

print("\n================================")
print("[FINAL ANSWER]\n")

print(final_response.choices[0].message.content)