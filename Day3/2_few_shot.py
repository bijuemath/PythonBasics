from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=""
)

# Few-Shot Prompt
few_shot_prompt = """
Convert variable names to camelCase.

Input: first_name
Output: firstName

Input: employee_salary
Output: employeeSalary

Input: total_amount
Output:
"""

# API call
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful programming assistant."
        },
        {
            "role": "user",
            "content": few_shot_prompt
        }
    ],
    temperature=0
)

# Print response
print(response.choices[0].message.content)