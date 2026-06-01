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
# SHORT-TERM MEMORY
# -----------------------------------

short_term_memory = []

# -----------------------------------
# LONG-TERM MEMORY FILE
# -----------------------------------

MEMORY_FILE = "long_term_memory.json"


# -----------------------------------
# CREATE MEMORY FILE IF NOT EXISTS
# -----------------------------------

if not os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)


# -----------------------------------
# SAVE TO LONG-TERM MEMORY
# -----------------------------------

def save_long_term_memory(data):

    with open(MEMORY_FILE, "r") as f:
        memories = json.load(f)

    # -----------------------------------
    # DUPLICATE CHECK
    # -----------------------------------

    if data not in memories:

        memories.append(data)

        with open(MEMORY_FILE, "w") as f:
            json.dump(memories, f, indent=4)

        return "Memory stored successfully"

    else:

        return "Memory already exists"

# -----------------------------------
# LOAD LONG-TERM MEMORY
# -----------------------------------

def load_long_term_memory():

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


# -----------------------------------
# MEMORY SEARCH TOOL
# -----------------------------------

def search_memory(query):

    memories = load_long_term_memory()

    results = []

    for memory in memories:

        if query.lower() in memory.lower():

            results.append(memory)

    return results


# -----------------------------------
# STORE MEMORY TOOL
# -----------------------------------

def store_memory(text):

    save_long_term_memory(text)

    return "Memory stored successfully"


# -----------------------------------
# TOOLS
# -----------------------------------

tools = [

    {
        "type": "function",
        "function": {
            "name": "store_memory",
            "description": "Store important user information permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string"
                    }
                },
                "required": ["text"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": "Search stored user information like name, favorite language, city, preferences, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# -----------------------------------
# AGENT LOOP
# -----------------------------------

print("\n========== AGENT START ==========\n")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    # -----------------------------------
    # SHORT-TERM MEMORY UPDATE
    # -----------------------------------

    short_term_memory.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    print("\n[SHORT-TERM MEMORY]")
    print(short_term_memory)

    # -----------------------------------
    # SYSTEM PROMPT
    # -----------------------------------

    system_prompt = """
    You are an intelligent AI assistant.

    Rules:
    1. Use store_memory tool for important personal information.
    2. Use search_memory tool when user asks about past information.
    3. Think step-by-step.
    """

    # -----------------------------------
    # LLM CALL
    # -----------------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + short_term_memory,

        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # -----------------------------------
    # TOOL CALLING
    # -----------------------------------

    if message.tool_calls:

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\n[AGENT THINKING]")
            print(f"Using Tool: {tool_name}")

            print("Arguments:", arguments)

            # -----------------------------------
            # STORE MEMORY TOOL
            # -----------------------------------

            if tool_name == "store_memory":

                result = store_memory(
                    arguments["text"]
                )

            # -----------------------------------
            # SEARCH MEMORY TOOL
            # -----------------------------------

            elif tool_name == "search_memory":

                result = search_memory(
                    arguments["query"]
                )

            else:
                result = "Unknown tool"

            print("\n[TOOL RESULT]")
            print(result)

            # -----------------------------------
            # FINAL RESPONSE
            # -----------------------------------

            final_response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    }

                ] + short_term_memory + [

                    message,

                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    }
                ]
            )

            assistant_reply = (
                final_response
                .choices[0]
                .message
                .content
            )

    else:

        assistant_reply = message.content

    # -----------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------

    print("\nAssistant:", assistant_reply)

    # -----------------------------------
    # SAVE TO SHORT-TERM MEMORY
    # -----------------------------------

    short_term_memory.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    # -----------------------------------
# DYNAMIC SHORT-TERM MEMORY SEARCH
# -----------------------------------

handled = False

keywords = ["name", "favorite", "city"]

if any(word in user_input.lower() for word in keywords):

    for item in reversed(short_term_memory):

        content = item["content"].lower()

        # SEARCH FOR NAME
        if "name" in user_input.lower():

            if "my name is" in content:

                name = item["content"].split("is")[-1].strip()

                print(f"\nAssistant: Your name is {name}")

                handled = True
                break

        # SEARCH FOR FAVORITE
        elif "favorite" in user_input.lower():

            if "favorite" in content:

                print(f"\nAssistant: {item['content']}")

                handled = True
                break

        if handled:
            continue