import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")
print (f"API Key: {api_key}")
# Create client
client = Groq(api_key=api_key)

# Test request
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)