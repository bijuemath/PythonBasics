import os
from dotenv import load_dotenv

from crewai import Agent
from crewai import Task
from crewai import Crew
from crewai import Process
from crewai import LLM

# ==================================================
# LOAD ENV
# ==================================================

load_dotenv()

# ==================================================
# OPENROUTER GPT4O MINI
# ==================================================

llm = LLM(
   model="openrouter/openai/gpt-4o-mini",
   base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==================================================
# BUSINESS ANALYST
# ==================================================

business_analyst = Agent(
    role="Business Analyst",
    goal="""
    Analyze business requirements and
    identify functional requirements.
    """,
    backstory="""
    Expert in gathering requirements
    from stakeholders.
    """,
    llm=llm,
    verbose=True,
    max_iter=3
)

# ==================================================
# ARCHITECT
# ==================================================

architect = Agent(
    role="Solution Architect",
    goal="""
    Create architecture based on requirements.
    """,
    backstory="""
    Expert in microservices,
    APIs, cloud and AI systems.
    """,
    llm=llm,
    verbose=True,
    max_iter=3
)

# ==================================================
# DEVELOPER
# ==================================================

developer = Agent(
    role="Senior Python Developer",
    goal="""
    Create production-ready Python code.
    """,
    backstory="""
    15 years of Python experience.
    """,
    llm=llm,
    verbose=True,
    max_iter=3
)

# ==================================================
# QA
# ==================================================

qa = Agent(
    role="QA Engineer",
    goal="""
    Review code and identify bugs.
    """,
    backstory="""
    Expert in testing and code review.
    """,
    llm=llm,
    verbose=True,
    max_iter=3
)

# ==================================================
# DOCUMENTATION
# ==================================================

writer = Agent(
    role="Technical Writer",
    goal="""
    Create technical documentation.
    """,
    backstory="""
    Expert documentation specialist.
    """,
    llm=llm,
    verbose=True,
    max_iter=3
)

# ==================================================
# MANAGER
# ==================================================

manager = Agent(
    role="Project Manager",
    goal="""
    Deliver ONE final software project report.

    Delegate work to specialists.
    Ensure tasks are completed.
    Stop after final report is produced.
    """,
    backstory="""
    Senior project manager with
    extensive software delivery experience.
    """,
    llm=llm,
    allow_delegation=False,
    verbose=True,
    max_iter=5
)

# ==================================================
# TASKS
# ==================================================

requirements_task = Task(
    description="""
    Build a Library Management System.

    Analyze:
    - Functional requirements
    - Non-functional requirements
    - User roles
    - System constraints
    """,
    expected_output="Requirements document"
)

architecture_task = Task(
    description="""
    Design architecture for the Library
    Management System.

    Include:
    - Components
    - Database
    - API Design
    - Security
    - Deployment
    """,
    expected_output="Architecture design"
)

development_task = Task(
    description="""
    Generate Python FastAPI implementation.

    Include:
    - Models
    - CRUD APIs
    - Validation
    """,
    expected_output="Python code"
)

testing_task = Task(
    description="""
    Review generated code.

    Identify:
    - Bugs
    - Security issues
    - Performance concerns
    """,
    expected_output="QA review report"
)

documentation_task = Task(
    description="""
    Create final documentation.

    Include:
    - Overview
    - Architecture
    - API Documentation
    - Deployment guide
    """,
    expected_output="Technical documentation"
)

# ==================================================
# CREW
# ==================================================

crew = Crew(
    agents=[
        business_analyst,
        architect,
        developer,
        qa,
        writer
    ],
    tasks=[
        requirements_task,
        architecture_task,
        development_task,
        testing_task,
        documentation_task
    ],
    manager_agent=manager,
    process=Process.hierarchical,
    verbose=True
)

# ==================================================
# EXECUTE
# ==================================================

result = crew.kickoff()

print("\n")
print("=" * 80)
print("FINAL RESULT")
print("=" * 80)
print(result)