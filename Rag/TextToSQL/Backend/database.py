import pyodbc
import pandas as pd

DB_PATH = r"D:\AgenticAI\Repo\PythonBasics\Rag\TextToSQL\Backend\company.accdb"


def get_connection():

    connection_string = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={DB_PATH};"
    )

    conn = pyodbc.connect(connection_string)

    return conn


# =========================
# Run SQL Query
# =========================
def run_query(query):

    conn = get_connection()

    try:
        df = pd.read_sql(query, conn)
        return df

    finally:
        conn.close()