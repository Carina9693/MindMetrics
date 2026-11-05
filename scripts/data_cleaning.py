
import pandas as pd
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "student_depression.csv"
OUTPUT_PATH = BASE_DIR / "data" / "student_depression_cleaned.csv"

# Load dataset
df = pd.read_csv(INPUT_PATH)

print("Original dataset shape:", df.shape)

# Standardize column names
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

# Remove leading/trailing spaces from text values
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip()

# Check missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Remove duplicate records
duplicates = df.duplicated().sum()
print("\nDuplicate records:", duplicates)

df = df.drop_duplicates()

# Handle missing values
for column in df.columns:
    if df[column].isnull().any():
        if df[column].dtype == "object":
            df[column] = df[column].fillna(df[column].mode()[0])
        else:
            df[column] = df[column].fillna(df[column].median())

# Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nCleaning completed!")
print("Cleaned dataset shape:", df.shape)
print("Saved to:", OUTPUT_PATH)
