from openai import OpenAI

client = OpenAI(
    api_key=""
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    max_tokens=20
)

print(response.choices[0].message.content)