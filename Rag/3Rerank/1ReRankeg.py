from sentence_transformers import CrossEncoder

# Load model
model = CrossEncoder(
    'cross-encoder/ms-marco-MiniLM-L-6-v2'
)

query = "How to reset password?"

documents = [
    "Password policy requires 8 characters.",
    "You can reset password using email OTP.",
    "Account settings page allows theme change."
]

# Create query-document pairs
pairs = [[query, doc] for doc in documents]

# Predict relevance scores
scores = model.predict(pairs)

# Combine document with score
results = list(zip(documents, scores))

# Sort by score descending
results = sorted(results, key=lambda x: x[1], reverse=True)

# Print reranked results
for doc, score in results:
    print(f"\nScore: {score:.4f}")
    print(doc)