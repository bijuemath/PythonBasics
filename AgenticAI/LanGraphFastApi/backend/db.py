import pyodbc
import pandas as pd

DB_PATH = r"../database/shop.accdb"

CONN_STR = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={DB_PATH};"
)

def execute_query(query):
    print(f"DEBUG: Executing query: {query}")
    conn = pyodbc.connect(CONN_STR)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame.from_records(data, columns=columns)
        return df.to_dict(orient="records")

    finally:
        conn.close()


def execute_update(query):
    print(f"DEBUG: Executing update query: {query}")
    conn = pyodbc.connect(CONN_STR)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows_affected = cursor.rowcount
        conn.commit()

        return f"Success: {rows_affected} rows affected."

    finally:
        conn.close()


def get_tables():

    conn = pyodbc.connect(CONN_STR)

    cursor = conn.cursor()

    tables = []

    for row in cursor.tables(tableType='TABLE'):
        tables.append(row.table_name)

    conn.close()

    return tables