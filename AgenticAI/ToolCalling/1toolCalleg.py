from groq import Groq
from dotenv import load_dotenv
import json
import re
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# TOOL 1 : Calculator
# -----------------------------
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# TOOL 2 : Weather Tool
# -----------------------------
def get_weather(city):
    weather_data = {
        "Delhi": "38°C",
        "Mumbai": "32°C",
        "Chennai": "35°C"
    }

    return weather_data.get(city, "Weather data not found")


# -----------------------------
# AVAILABLE TOOLS
# -----------------------------
tools = [

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate math expressions",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
# -----------------------------
# USER QUESTION
# -----------------------------
#user_question = "What is 100 + 200?"
user_question = "What is the weather in Delhi?"


# -----------------------------
# SEND TO LLM
# -----------------------------
response = client.chat.completions.create(
     model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
             "content": user_question
        }
    ],
    tools=tools,
    tool_choice="auto"
)

# -----------------------------
# CHECK TOOL CALL
# -----------------------------
message = response.choices[0].message

if message.tool_calls:

    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name

    arguments = json.loads(tool_call.function.arguments)

    print("\nTool Selected:", tool_name)
    print("Arguments:", arguments)


    # -----------------------------
    # EXECUTE TOOL
    # -----------------------------
    if tool_name == "calculator":

        result = calculator(arguments["expression"])

    elif tool_name == "get_weather":

        result = get_weather(arguments["city"])

    else:
        result = "Unknown tool"


    print("\nTool Result:", result)


    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": user_question
            },
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            }
        ]
    )

    print("\nFinal Answer:")
    print(final_response.choices[0].message.content)

else:
    print(response.choices[0].message.content)