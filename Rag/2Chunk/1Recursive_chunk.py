from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Artificial Intelligence is transforming industries.

Machine learning helps systems learn from data.

Deep learning uses neural networks.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,
    chunk_overlap=10
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}:")
    print(chunk)