from groq import Groq

client = Groq(
    api_key=""
)

def generate_tagline(temperature):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": "Write a tagline for a AI  Traning by Biju"
            }
        ]
    )

    return response.choices[0].message.content


# Example usage
print ("deterministic and focused")
print ("--------------------------")
print(generate_tagline(0))

print ("\nbalanced creativity")
print ("--------------------------")
print(generate_tagline(0.7))

print ("\nhighly creative/random")
print ("--------------------------")

print(generate_tagline(1.6))