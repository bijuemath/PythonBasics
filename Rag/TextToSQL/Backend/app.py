from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from database import run_query

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str
    groq_key: str


# =========================
# Database Schema Prompt
# =========================
SCHEMA = """
You are an expert Microsoft Access SQL assistant.

Database Schema:

Table: customers
- customer_id
- customer_name
- city

Table: products
- product_id
- product_name
- price

Table: orders
- order_id
- customer_id
- product_id
- quantity
- order_date

Relations:
- orders.customer_id = customers.customer_id
- orders.product_id = products.product_id

Rules:
1. Generate only Microsoft Access SQL.
2. Use nested INNER JOIN syntax.
3. Use parentheses for joins.
4. Always wrap text values in single quotes.
5. Generate only SELECT queries.
6. Do not provide explanation.
7. Do not use markdown.
8. Return only SQL query.
"""

@app.get("/")
def home():
    return {"message": "SQL Text RAG API Running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        client = Groq(api_key=request.groq_key)

        # =========================
        # Generate SQL Query
        # =========================
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SCHEMA
                },
                {
                    "role": "user",
                    "content": request.question
                }
            ],
             temperature=0
        )

        generated_sql = response.choices[0].message.content.strip()

        # Remove markdown if present
        generated_sql = generated_sql.replace("```sql", "")
        generated_sql = generated_sql.replace("```", "")

        # =========================
        # Execute SQL Query
        # =========================
        result_df = run_query(generated_sql)

        # =========================
        # Convert Result to JSON
        # =========================
        result_json = result_df.to_dict(orient="records")

        return {
            "question": request.question,
            "generated_sql": generated_sql,
            "result": result_json
        }
    except Exception as e:
        return {
            "error": str(e)
        }