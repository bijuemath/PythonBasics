from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

sentences = [
    "Python is a programming language.",
    "It supports object oriented programming.",
    "Bananas are rich in potassium.",
    "Apples contain fiber."
]

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(sentences)

threshold = 0.6
chunks = []
current_chunk = [sentences[0]]

for i in range(1, len(sentences)):
    similarity = cosine_similarity(
        [embeddings[i-1]],
        [embeddings[i]]
    )[0][0]

    if similarity > threshold:
        current_chunk.append(sentences[i])
    else:
        chunks.append(current_chunk)
        current_chunk = [sentences[i]]

chunks.append(current_chunk)

for idx, chunk in enumerate(chunks):
    print(f"\nChunk {idx+1}:")
    print(" ".join(chunk))