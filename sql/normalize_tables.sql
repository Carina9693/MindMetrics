

DROP TABLE IF EXISTS mental_health;
DROP TABLE IF EXISTS academic_wellbeing;
DROP TABLE IF EXISTS students;

-- 1. Student information
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    gender TEXT,
    age INTEGER,
    family_history_mental_illness TEXT
);

INSERT INTO students
SELECT
    student_id,
    gender,
    age,
    family_history_mental_illness
FROM student_data;

-- 2. Academic and lifestyle information
CREATE TABLE academic_wellbeing (
    student_id INTEGER PRIMARY KEY,
    academic_pressure REAL,
    study_satisfaction REAL,
    sleep_duration TEXT,
    dietary_habits TEXT,
    study_hours INTEGER,
    financial_stress REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

INSERT INTO academic_wellbeing
SELECT
    student_id,
    academic_pressure,
    study_satisfaction,
    sleep_duration,
    dietary_habits,
    study_hours,
    financial_stress
FROM student_data;

-- 3. Mental health outcomes
CREATE TABLE mental_health (
    student_id INTEGER PRIMARY KEY,
    suicidal_thoughts TEXT,
    depression TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

INSERT INTO mental_health
SELECT
    student_id,
    suicidal_thoughts,
    depression
FROM student_data;
