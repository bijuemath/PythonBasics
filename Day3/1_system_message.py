from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=""
)

# System message example
system_message = """
You are a senior Python developer.
Always provide:
- clean code
- beginner-friendly explanations
- optimized solutions
"""

# User prompt
user_prompt = "Write a Python function to check whether a number is even or odd."

# API call
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    temperature=0
)

# Print response
print(response.choices[0].message.content)