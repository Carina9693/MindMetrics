
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "student_depression_cleaned.csv"
CHART_PATH = BASE_DIR / "reports" / "charts"

CHART_PATH.mkdir(parents=True, exist_ok=True)

# Load cleaned data
df = pd.read_csv(DATA_PATH)

sns.set_theme(style="whitegrid")

print("MINDMETRICS - EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# 1. Basic dataset information
print("\nDataset Shape:", df.shape)
print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe(include="all").to_string())

# 2. Depression distribution
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="depression")
plt.title("Student Depression Distribution")
plt.xlabel("Depression Status")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(CHART_PATH / "depression_distribution.png")
plt.close()

# 3. Depression by gender
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="gender", hue="depression")
plt.title("Depression Distribution by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(CHART_PATH / "depression_by_gender.png")
plt.close()

# 4. Academic pressure analysis
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="depression", y="academic_pressure")
plt.title("Academic Pressure by Depression Status")
plt.xlabel("Depression Status")
plt.ylabel("Academic Pressure")
plt.tight_layout()
plt.savefig(CHART_PATH / "academic_pressure.png")
plt.close()

# 5. Sleep duration analysis
plt.figure(figsize=(9, 5))
sns.countplot(data=df, x="sleep_duration", hue="depression")
plt.title("Sleep Duration and Depression")
plt.xlabel("Sleep Duration")
plt.ylabel("Number of Students")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(CHART_PATH / "sleep_duration.png")
plt.close()

# 6. Financial stress analysis
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="depression", y="financial_stress")
plt.title("Financial Stress by Depression Status")
plt.xlabel("Depression Status")
plt.ylabel("Financial Stress")
plt.tight_layout()
plt.savefig(CHART_PATH / "financial_stress.png")
plt.close()

# 7. Study hours analysis
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="depression", y="study_hours")
plt.title("Study Hours by Depression Status")
plt.xlabel("Depression Status")
plt.ylabel("Study Hours")
plt.tight_layout()
plt.savefig(CHART_PATH / "study_hours.png")
plt.close()

# 8. Study satisfaction analysis
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="depression", y="study_satisfaction")
plt.title("Study Satisfaction by Depression Status")
plt.xlabel("Depression Status")
plt.ylabel("Study Satisfaction")
plt.tight_layout()
plt.savefig(CHART_PATH / "study_satisfaction.png")
plt.close()

print("\nEDA completed successfully!")
print("Charts saved in:", CHART_PATH)
