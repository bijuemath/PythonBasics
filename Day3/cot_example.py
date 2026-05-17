from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=""
)

# Prompt 1: Normal Prompt
normal_prompt = """
A shop had 45 chocolates.
It sold 18 chocolates and then added 12 more.
How many chocolates are left?
"""

# Prompt 2: Chain of Thought Prompt
cot_prompt = """
Think step-by-step and solve:

A shop had 45 chocolates.
It sold 18 chocolates and then added 12 more.
How many chocolates are left?
"""


# Function to get model response
def get_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# Run both prompts
normal_result = get_response(normal_prompt)
cot_result = get_response(cot_prompt)

# Print outputs
print("========== NORMAL PROMPT ==========")
print(normal_result)

print("\n========== COT PROMPT ==========")
print(cot_result)