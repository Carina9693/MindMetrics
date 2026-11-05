import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "mindmetrics.db"
SQL_PATH = BASE_DIR / "sql" / "normalize_tables.sql"

connection = sqlite3.connect(DB_PATH)

try:
    connection.execute("PRAGMA foreign_keys = ON")

    with open(SQL_PATH, "r", encoding="utf-8") as file:
        sql_script = file.read()

    connection.executescript(sql_script)

    print("Database normalization completed!")

    for table in ["students", "academic_wellbeing", "mental_health"]:
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count} records")

finally:
    connection.close()