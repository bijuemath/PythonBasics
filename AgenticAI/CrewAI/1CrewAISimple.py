from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
   model="openrouter/openai/gpt-4o-mini",
   base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


agent = Agent(
    role="Assistant",
    goal="Answer questions",
    backstory="Helpful AI assistant",
    llm=llm,
    verbose=True
)

task = Task(
    description="Explain Agentic AI in 5 sentences.",
    expected_output="A concise explanation of Agentic AI.",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

print("\n=== RESULT ===")
print(result)