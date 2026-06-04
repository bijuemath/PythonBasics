from db import execute_query

SCHEMA = """
customers
(
 customer_id,
 customer_name,
 city
)

products
(
 product_id,
 product_name,
 price
)

orders
(
 order_id,
 customer_id,
 product_id,
 quantity,
 order_date
)
"""

def generate_sql(question, llm):

    prompt = f"""
You are a SQL expert specializing in Microsoft Access.

Database Schema:

{SCHEMA}

Generate a simple, valid SQL query to answer the user's question.
For INSERT queries, use the 'INSERT INTO ... SELECT ...' syntax.
IMPORTANT: The 'SELECT' part MUST include a 'FROM' clause, even if selecting constants (e.g., 'SELECT 1, 2 FROM customers WHERE ...'). You can use a table like 'customers' in the FROM clause to satisfy this.
If joining multiple tables, YOU MUST USE PARENTHESES AROUND JOIN CLAUSES (e.g., SELECT * FROM (TableA INNER JOIN TableB ON TableA.id = TableB.id) INNER JOIN TableC ON TableB.id = TableC.id).
Do not use backticks or markdown formatting in the output.
Only return the SQL query string.

Question:
{question}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()
    # Remove markdown formatting if present
    if content.startswith("```"):
        content = content.replace("```sql", "").replace("```", "").strip()
    return content