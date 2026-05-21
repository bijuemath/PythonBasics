import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------------
# Full Quantum Computing Text
# -----------------------------------

text = """
A quantum computer is a real or theoretical computer that exploits quantum phenomena like superposition and entanglement in an essential way.

The basic unit of information in quantum computing, the qubit (or quantum bit), serves the same function as the bit in ordinary or classical computing.

Quantum parallelism is the heuristic that quantum computers can be thought of as evaluating a function for multiple input values simultaneously.

A quantum gate array decomposes computation into a sequence of few-qubit quantum gates.
"""

# -----------------------------------
# Simple Chunking
# Split using empty lines
# -----------------------------------

chunks = text.strip().split("\n\n")

print("Chunks Created:\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print("-" * 50)

# -----------------------------------
# Create ChromaDB Client
# -----------------------------------

#client = chromadb.Client()

client = chromadb.PersistentClient(
    path="D:\\AgenticAI\\Repo\PythonBasics\\Rag\\1VecotorDB\\chroma_db"
)

# Create collection
collection = client.get_or_create_collection(name="quantum_notes")

# -----------------------------------
# Load Embedding Model
# -----------------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert chunks into embeddings
embeddings = model.encode(chunks).tolist()

# -----------------------------------
# Store Chunks
# -----------------------------------

ids = [str(i) for i in range(len(chunks))]

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)

print("\nChunks stored successfully!")

# -----------------------------------
# User Query
# -----------------------------------

query = "What is qubit?"

# Convert query to embedding
query_embedding = model.encode([query]).tolist()

# -----------------------------------
# Search Similar Chunks
# -----------------------------------

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

# -----------------------------------
# Display Results
# -----------------------------------

print("\nSearch Results:\n")

for doc in results["documents"][0]:
    print(doc)
    print("-" * 50)