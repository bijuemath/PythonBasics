from groq import Groq

client = Groq(
    api_key=""
)
def generate_tagline(top_p):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        top_p=top_p
        messages=[
            {
                "role": "user",
                "content": "Write a tagline for a coffee shop"
            }
        ]
    )

    return response.choices[0].message.content


# Example usage
print(generate_tagline(0))
print(generate_tagline(0.9))