from fastapi import FastAPI

from pydantic import BaseModel

from agent import agent

from fastapi.responses import JSONResponse
import traceback


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(req: QueryRequest):

    try:

        result = agent.invoke(
            {
                "user_query": req.query
            }
        )

        return {
            "response": result["response"]
        }

    except Exception as e:

        print(traceback.format_exc())

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "trace": traceback.format_exc()
            }
        )