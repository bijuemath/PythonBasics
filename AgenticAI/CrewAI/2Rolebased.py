import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process, LLM

# ---------------------------------------
# Load Environment
# ---------------------------------------

load_dotenv()

# ---------------------------------------
# OpenRouter LLM
# ---------------------------------------
llm = LLM(
   model="openrouter/openai/gpt-4o-mini",
   base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------
# Worker Agents
# ---------------------------------------

researcher = Agent(
    role="AI Researcher",
    goal="Research the given topic thoroughly",
    backstory="""
    Expert researcher who gathers facts,
    trends, advantages and challenges.
    """,
    llm=llm,
    verbose=True
)

architect = Agent(
    role="Solution Architect",
    goal="Design a technical architecture",
    backstory="""
    Senior software architect with expertise
    in distributed systems and Agentic AI.
    """,
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create professional documentation",
    backstory="""
    Expert technical writer who transforms
    technical content into readable reports.
    """,
    llm=llm,
    verbose=True
)

# ---------------------------------------
# Manager Agent
# ---------------------------------------

manager = Agent(
    role="Project Manager",
    goal="""
    Coordinate all agents and ensure
    the final deliverable is complete.
    """,
    backstory="""
    You are an experienced project manager.
    You decide which specialist should work
    on each task and verify output quality.
    """,
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------
# Tasks
# ---------------------------------------

research_task = Task(
    description="""
    Research Agentic AI systems.

    Include:
    - Definition
    - Components
    - Advantages
    - Challenges
    """,
    expected_output="Detailed research report"
)

architecture_task = Task(
    description="""
    Design an Agentic AI architecture.

    Include:
    - LLM
    - Memory
    - Planning
    - Tool Calling
    - Execution Loop
    - Human Feedback
    """,
    expected_output="Architecture document"
)

report_task = Task(
    description="""
    Create a final report combining
    all findings and architecture.
    """,
    expected_output="Professional report"
)

# ---------------------------------------
# Hierarchical Crew
# ---------------------------------------

crew = Crew(
    agents=[
        researcher,
        architect,
        writer
    ],
    tasks=[
        research_task,
        architecture_task,
        report_task
    ],
    manager_agent=manager,
    process=Process.hierarchical,
    verbose=True
)

# ---------------------------------------
# Run
# ---------------------------------------

result = crew.kickoff()

print("\n")
print("=" * 80)
print("FINAL OUTPUT")
print("=" * 80)
print(result)