
-- 1. Total number of students
SELECT COUNT(*) AS total_students
FROM student_data;

-- 2. Depression distribution
SELECT
    depression,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_data), 2) AS percentage
FROM student_data
GROUP BY depression;

-- 3. Depression by gender
SELECT
    gender,
    depression,
    COUNT(*) AS student_count
FROM student_data
GROUP BY gender, depression
ORDER BY gender, depression;

-- 4. Average academic pressure by depression status
SELECT
    depression,
    ROUND(AVG(academic_pressure), 2) AS avg_academic_pressure
FROM student_data
GROUP BY depression;

-- 5. Depression distribution by sleep duration
SELECT
    sleep_duration,
    depression,
    COUNT(*) AS student_count
FROM student_data
GROUP BY sleep_duration, depression
ORDER BY sleep_duration, depression;

-- 6. Financial stress by depression status
SELECT
    depression,
    ROUND(AVG(financial_stress), 2) AS avg_financial_stress
FROM student_data
GROUP BY depression;

-- 7. Average study hours by depression status
SELECT
    depression,
    ROUND(AVG(study_hours), 2) AS avg_study_hours
FROM student_data
GROUP BY depression;

-- 8. Depression by dietary habits
SELECT
    dietary_habits,
    depression,
    COUNT(*) AS student_count
FROM student_data
GROUP BY dietary_habits, depression;

-- 9. Family history and depression
SELECT
    family_history_mental_illness,
    depression,
    COUNT(*) AS student_count
FROM student_data
GROUP BY family_history_mental_illness, depression;

-- 10. Academic pressure and study satisfaction
SELECT
    depression,
    ROUND(AVG(academic_pressure), 2) AS avg_pressure,
    ROUND(AVG(study_satisfaction), 2) AS avg_satisfaction
FROM student_data
GROUP BY depression;


-- 1. INNER JOIN
SELECT
    s.student_id,
    s.gender,
    s.age,
    a.academic_pressure,
    a.study_satisfaction,
    m.depression
FROM students s
INNER JOIN academic_wellbeing a
    ON s.student_id = a.student_id
INNER JOIN mental_health m
    ON s.student_id = m.student_id
LIMIT 10;



-- 2. LEFT JOIN
SELECT
    s.student_id,
    s.gender,
    m.depression
FROM students s
LEFT JOIN mental_health m
    ON s.student_id = m.student_id;



-- 3. GROUP BY and HAVING
SELECT
    s.gender,
    COUNT(*) AS depressed_students
FROM students s
JOIN mental_health m
    ON s.student_id = m.student_id
WHERE m.depression = 'Yes'
GROUP BY s.gender
HAVING COUNT(*) > 100;


-- 4. CASE WHEN
SELECT
    CASE
        WHEN academic_pressure >= 4 THEN 'High Pressure'
        WHEN academic_pressure >= 2 THEN 'Moderate Pressure'
        ELSE 'Low Pressure'
    END AS pressure_category,
    COUNT(*) AS student_count
FROM academic_wellbeing
GROUP BY pressure_category;


SELECT
    student_id,
    academic_pressure
FROM academic_wellbeing
WHERE academic_pressure > (
    SELECT AVG(academic_pressure)
    FROM academic_wellbeing
)
ORDER BY academic_pressure DESC;

WITH student_analysis AS (
    SELECT
        m.depression,
        a.academic_pressure,
        a.study_satisfaction
    FROM mental_health m
    JOIN academic_wellbeing a
        ON m.student_id = a.student_id
)

SELECT
    depression,
    ROUND(AVG(academic_pressure), 2) AS avg_pressure,
    ROUND(AVG(study_satisfaction), 2) AS avg_satisfaction
FROM student_analysis
GROUP BY depression;

WITH pressure_analysis AS (
    SELECT student_id, academic_pressure
    FROM academic_wellbeing
    WHERE academic_pressure >= 4
),

financial_analysis AS (
    SELECT student_id, financial_stress
    FROM academic_wellbeing
    WHERE financial_stress >= 4
)

SELECT
    p.student_id,
    p.academic_pressure,
    f.financial_stress
FROM pressure_analysis p
INNER JOIN financial_analysis f
    ON p.student_id = f.student_id;


SELECT
    student_id,
    academic_pressure,
    RANK() OVER (
        ORDER BY academic_pressure DESC
    ) AS pressure_rank
FROM academic_wellbeing
LIMIT 20;


SELECT
    student_id,
    study_satisfaction,
    DENSE_RANK() OVER (
        ORDER BY study_satisfaction DESC
    ) AS satisfaction_rank
FROM academic_wellbeing
LIMIT 20;

SELECT
    s.student_id,
    m.depression,
    a.academic_pressure,
    ROW_NUMBER() OVER (
        PARTITION BY m.depression
        ORDER BY a.academic_pressure DESC
    ) AS row_num
FROM students s
JOIN academic_wellbeing a
    ON s.student_id = a.student_id
JOIN mental_health m
    ON s.student_id = m.student_id;

SELECT
    s.student_id,
    m.depression,
    a.academic_pressure,
    ROUND(
        AVG(a.academic_pressure) OVER (
            PARTITION BY m.depression
        ), 2
    ) AS category_avg_pressure
FROM students s
JOIN academic_wellbeing a
    ON s.student_id = a.student_id
JOIN mental_health m
    ON s.student_id = m.student_id
LIMIT 20;


SELECT
    student_id,
    academic_pressure,
    ROUND(
        AVG(academic_pressure) OVER (), 2
    ) AS overall_avg_pressure
FROM academic_wellbeing
LIMIT 20;

SELECT
    a.sleep_duration,
    COUNT(*) AS total_students,
    SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END) AS depressed_students,
    ROUND(
        100.0 * SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS depression_percentage
FROM academic_wellbeing a
JOIN mental_health m
    ON a.student_id = m.student_id
GROUP BY a.sleep_duration
ORDER BY depression_percentage DESC;

SELECT
    s.family_history_mental_illness,
    COUNT(*) AS total_students,
    SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END) AS depressed_students,
    ROUND(
        100.0 * SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS depression_percentage
FROM students s
JOIN mental_health m
    ON s.student_id = m.student_id
GROUP BY s.family_history_mental_illness;

SELECT
    CASE
        WHEN a.academic_pressure >= 4 THEN 'High'
        WHEN a.academic_pressure >= 2 THEN 'Moderate'
        ELSE 'Low'
    END AS pressure_category,
    COUNT(*) AS total_students,
    SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END) AS depressed_students,
    ROUND(
        100.0 * SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS depression_percentage
FROM academic_wellbeing a
JOIN mental_health m
    ON a.student_id = m.student_id
GROUP BY pressure_category;

SELECT
    a.dietary_habits,
    COUNT(*) AS total_students,
    SUM(CASE WHEN m.depression = 'Yes' THEN 1 ELSE 0 END) AS depressed_students
FROM academic_wellbeing a
JOIN mental_health m
    ON a.student_id = m.student_id
GROUP BY a.dietary_habits
ORDER BY depressed_students DESC;

SELECT
    s.student_id,
    s.gender,
    s.age,
    a.academic_pressure,
    a.financial_stress,
    a.sleep_duration,
    a.study_satisfaction,
    m.depression
FROM students s
JOIN academic_wellbeing a
    ON s.student_id = a.student_id
JOIN mental_health m
    ON s.student_id = m.student_id
ORDER BY a.academic_pressure DESC,
         a.financial_stress DESC;