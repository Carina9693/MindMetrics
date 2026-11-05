
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "mindmetrics.db"
SQL_PATH = BASE_DIR / "sql" / "analysis_queries.sql"

connection = sqlite3.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_script = file.read()

queries = [
    query.strip()
    for query in sql_script.split(";")
    if query.strip()
]

for i, query in enumerate(queries, start=1):
    print(f"\n{'=' * 50}")
    print(f"QUERY {i}")
    print("=" * 50)

    result = pd.read_sql_query(query, connection)
    print(result.to_string(index=False))

connection.close()
