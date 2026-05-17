import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()

# -----------------------------------
# Initialize Groq Client
# -----------------------------------

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------------
# Quantum Computing Content
# -----------------------------------

text = """
A quantum computer is a real or theoretical computer that exploits quantum phenomena like superposition and entanglement in an essential way.

The basic unit of information in quantum computing, the qubit (or quantum bit), serves the same function as the bit in ordinary or classical computing.

Quantum parallelism is the heuristic that quantum computers can be thought of as evaluating a function for multiple input values simultaneously.

A quantum gate array decomposes computation into a sequence of few-qubit quantum gates.
"""

# -----------------------------------
# Chunking
# -----------------------------------

chunks = text.strip().split("\n\n")

# -----------------------------------
# Create Persistent ChromaDB
# -----------------------------------

client_chroma = chromadb.PersistentClient(
    path="chroma_db"
)

# Create collection
collection = client_chroma.get_or_create_collection(
    name="quantum_notes"
)

# -----------------------------------
# Load Embedding Model
# -----------------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------------
# Store Data (Only First Time)
# -----------------------------------

if collection.count() == 0:

    embeddings = model.encode(chunks).tolist()

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    print("Documents stored in ChromaDB!")

# -----------------------------------
# User Question
# -----------------------------------

query = "What is qubit?"

# Convert query into embedding
query_embedding = model.encode([query]).tolist()

# -----------------------------------
# Retrieve Similar Chunks
# -----------------------------------

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

retrieved_docs = results["documents"][0]

# Combine retrieved chunks
context = "\n".join(retrieved_docs)

print("\nRetrieved Context:\n")
print(context)

# -----------------------------------
# Create Prompt for LLM
# -----------------------------------

prompt = f"""
Answer the question using the below context only.

Context:
{context}

Question:
{query}
"""

# -----------------------------------
# Generate Answer using Groq
# -----------------------------------

response = client_groq.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# -----------------------------------
# Final Output
# -----------------------------------

answer = response.choices[0].message.content

print("\nFinal Answer:\n")
print(answer)