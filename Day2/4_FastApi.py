from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the data structure for the request
class DataInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/process")
def process_data(input_data: DataInput):
    # Logic happens here (e.g., AI processing, DB queries)
    result = f"Processed: {input_data.text.upper()}"
    return {"message": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("4_FastApi:app", host="127.0.0.1", port=8000, reload=True)