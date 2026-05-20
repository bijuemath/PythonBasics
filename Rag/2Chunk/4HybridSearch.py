from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

documents = [
    "Python supports machine learning",
    "Bananas are healthy fruits",
    "Deep learning uses neural networks"
]

query = "AI and neural networks"

# ------------------------
# BM25
# ------------------------

tokenized_docs = [doc.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

bm25_scores = bm25.get_scores(query.split())

# ------------------------
# Vector Search
# ------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')

doc_embeddings = model.encode(documents)
query_embedding = model.encode([query])

vector_scores = cosine_similarity(
    query_embedding,
    doc_embeddings
)[0]

# ------------------------
# Hybrid Score
# ------------------------

hybrid_scores = (
    0.5 * np.array(bm25_scores) +
    0.5 * np.array(vector_scores)
)

# Ranking
ranked_docs = sorted(
    zip(documents, hybrid_scores),
    key=lambda x: x[1],
    reverse=True
)

for doc, score in ranked_docs:
    print(score, "->", doc)