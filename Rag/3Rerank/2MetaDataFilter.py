import chromadb

# Create client
client = chromadb.Client()

# Create collection
collection = client.create_collection("resume_search")

# Resume texts
documents = [
    """
    I am Steve Smith with 12 years of experience in .NET Core.
    I work at Google in San Francisco.
    My email id is steve.smith@gmail.com.
    """,

    """
    I am John Miller with 5 years of experience in Python and Django.
    I work at Amazon in Seattle.
    My email id is john.miller@gmail.com.
    """,
     """
    I am Peter Mc with 7 years of experience in  .NET Core.
    I work at Microsoft  in Newyork.
    My email id is peter.mc@gmail.com.
    """
]

# Metadata
metadatas = [
    {
        "candidate_name": "Steve Smith",
        "experience": 12,
        "skill": ".NET Core",
        "company": "Google",
        "location": "San Francisco",
        "email": "steve.smith@gmail.com"
    },

    {
        "candidate_name": "John Miller",
        "experience": 5,
        "skill": "Python",
        "company": "Amazon",
        "location": "Seattle",
        "email": "john.miller@gmail.com"
    },

    {
        "candidate_name": "Peter Mc",
        "experience": 7,
        "skill": ".NET Core",
        "company": "Microsoft",
        "location": "New York",
        "email": "peter.mc@gmail.com"
    }
]

# IDs
ids = ["1", "2", "3"]

# Add to collection
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("Resume data stored successfully")


results = collection.query(
    query_texts=[".NET developer"],
    n_results=5,

    where={
        "company": "Google"
    }
)

print(results)