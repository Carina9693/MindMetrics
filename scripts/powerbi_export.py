import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "student_depression_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "dashboard" / "powerbi_data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(DATA_PATH)

# 1. Export main dataset
df.to_csv(OUTPUT_DIR / "student_analysis.csv", index=False)

# 2. Depression summary
depression_summary = (
    df.groupby("depression")
    .size()
    .reset_index(name="student_count")
)

depression_summary["percentage"] = (
    depression_summary["student_count"] / len(df) * 100
).round(2)

depression_summary.to_csv(
    OUTPUT_DIR / "depression_summary.csv", index=False
)

# 3. Gender analysis
gender_analysis = (
    df.groupby(["gender", "depression"])
    .size()
    .reset_index(name="student_count")
)

gender_analysis.to_csv(
    OUTPUT_DIR / "gender_analysis.csv", index=False
)

# 4. Academic and financial analysis
factor_analysis = (
    df.groupby("depression")
    .agg(
        avg_academic_pressure=("academic_pressure", "mean"),
        avg_study_satisfaction=("study_satisfaction", "mean"),
        avg_financial_stress=("financial_stress", "mean"),
        avg_study_hours=("study_hours", "mean")
    )
    .round(2)
    .reset_index()
)

factor_analysis.to_csv(
    OUTPUT_DIR / "factor_analysis.csv", index=False
)

# 5. Sleep analysis
sleep_analysis = (
    df.groupby(["sleep_duration", "depression"])
    .size()
    .reset_index(name="student_count")
)

sleep_analysis.to_csv(
    OUTPUT_DIR / "sleep_analysis.csv", index=False
)

print("Power BI datasets exported successfully!")
print("\nFiles created:")
for file in OUTPUT_DIR.iterdir():
    print(file.name)

print("\nTotal student records:", len(df))



import sqlite3

DB_PATH = BASE_DIR / "data" / "mindmetrics.db"

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    s.student_id,
    s.gender,
    s.age,
    s.family_history_mental_illness,
    a.academic_pressure,
    a.study_satisfaction,
    a.sleep_duration,
    a.dietary_habits,
    a.study_hours,
    a.financial_stress,
    m.suicidal_thoughts,
    m.depression
FROM students s
JOIN academic_wellbeing a
    ON s.student_id = a.student_id
JOIN mental_health m
    ON s.student_id = m.student_id
"""

combined_df = pd.read_sql_query(query, connection)

connection.close()

combined_df.to_csv(
    OUTPUT_DIR / "mindmetrics_final.csv",
    index=False
)

print("\nCombined SQL dataset exported!")
print("Total records:", len(combined_df))