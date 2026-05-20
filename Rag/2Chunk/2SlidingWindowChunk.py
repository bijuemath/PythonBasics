from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Python is widely used for Artificial Intelligence and Machine Learning.
It is also popular in Data Science and Automation.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}:")
    print(chunk)