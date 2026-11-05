import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "student_depression.csv"
DB_PATH = BASE_DIR / "data" / "mindmetrics.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

# Connect to SQLite database
connection = sqlite3.connect(DB_PATH)

try:
    # Read dataset
    df = pd.read_csv(DATA_PATH)

    # Rename columns for SQL convenience
    df.columns = [
        "gender",
        "age",
        "academic_pressure",
        "study_satisfaction",
        "sleep_duration",
        "dietary_habits",
        "suicidal_thoughts",
        "study_hours",
        "financial_stress",
        "family_history_mental_illness",
        "depression"
    ]

    # Recreate table using schema.sql
    connection.execute("DROP TABLE IF EXISTS student_data")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    # Import dataset
    df.to_sql("student_data", connection, if_exists="append", index=False)

    # Verify imported records
    count = pd.read_sql_query(
        "SELECT COUNT(*) AS total_students FROM student_data",
        connection
    )

    print("Database created successfully!")
    print(count)

    print("\nSample records:")
    print(pd.read_sql_query(
        "SELECT * FROM student_data LIMIT 5",
        connection
    ))

finally:
    connection.close()