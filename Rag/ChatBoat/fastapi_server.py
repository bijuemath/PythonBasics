from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import uuid
import shutil

from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer

import lancedb
import pandas as pd

from groq import Groq

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Create Upload Folder
# -------------------------------------------------

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# Embedding Model
# -------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -------------------------------------------------
# LanceDB Setup
# -------------------------------------------------

DB_PATH = "lancedb_data"
db = lancedb.connect(DB_PATH)

TABLE_NAME = "documents"

try:
    table = db.open_table(TABLE_NAME)
except:
    df = pd.DataFrame([
        {
            "id": "1",
            "text": "dummy",
            "vector": [0.0] * 384
        }
    ])

    table = db.create_table(TABLE_NAME, data=df)

# -------------------------------------------------
# Text Splitter
# -------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# -------------------------------------------------
# Upload API
# -------------------------------------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Chunking
    chunks = splitter.split_documents(docs)

    rows = []

    for chunk in chunks:

        text = chunk.page_content

        embedding = embedding_model.encode(text).tolist()

        rows.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "vector": embedding
        })

    df = pd.DataFrame(rows)

    table.add(df)

    return {
        "message": f"{file.filename} uploaded successfully",
        "chunks": len(rows)
    }

# -------------------------------------------------
# Query Request Model
# -------------------------------------------------

class QueryRequest(BaseModel):
     question: str
     groq_key: str

# -------------------------------------------------
# Ask API
# -------------------------------------------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    question = request.question
    groq_key = request.groq_key

    # Create Query Embedding
    query_embedding = embedding_model.encode(question).tolist()

    # Search Similar Chunks
    results = (
        table.search(query_embedding)
        .limit(3)
        .to_list()
    )

    if len(results) == 0:
        return {
            "answer": "Not found in uploaded document."
        }
    context = "\n\n".join([ r["text"] for r in results])
       
    

    # Basic Similarity Check
    top_text = results[0]["text"]

    if len(top_text.strip()) < 20:
        return {
            "answer": "Not found in uploaded document."
        }

    # Prompt
    prompt = f"""
You are a document assistant.

Answer ONLY from the provided context.

If the answer is not present in context,
reply exactly:
Not found in uploaded document.

Context:
{context}
Question:
{question}
"""

    # Groq Client
    client = Groq(api_key=groq_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer
    }
# -------------------------------------------------
# Root API
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "RAG Document Finder API Running"
    }

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )