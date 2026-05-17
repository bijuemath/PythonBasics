from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Intelligence Engine")

class AnalysisRequest(BaseModel):
    content: str
    analysis_type: str = "summary"

@app.get("/")
def health_check():
    return {"status": "online", "engine": "Python 3.10"}

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    if not request.content:
        raise HTTPException(status_code=400, detail="No content provided")

    # Simulate complex AI processing time
    time.sleep(1.5) 
    
    word_count = len(request.content.split())
    sentiment = "Positive" if word_count % 2 == 0 else "Neutral"
    
    return {
        "analysis": f"Completed {request.analysis_type} for {word_count} words.",
        "metrics": {
            "sentiment": sentiment,
            "complexity_score": round(word_count * 0.12, 2)
        },
        "tags": ["AI-Generated", "Processed"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("6_api:app", host="127.0.0.1", port=8000, reload=True)