experience_category_query = """
SELECT ap.name, ap.phone, ap.email
FROM cv
JOIN applicant ap ON cv.applicant_id = ap.id
JOIN experience exp ON exp.cv_id = cv.id
WHERE exp.category=%s AND EXTRACT(YEAR FROM AGE(exp.end_date, exp.start_date)) = %s;
"""

city_query = """
SELECT name, phone, email
FROM applicant
WHERE applicant.city=%s;
"""

all_skills_query = """
SELECT ap.name, ap.phone, ap.email
FROM cv
JOIN applicant ap ON cv.applicant_id = ap.id
JOIN cv_skill ON cv.id = cv_skill.cv_id
JOIN skill s ON s.id = cv_skill.skill_id
WHERE s.name = ANY(%s)
GROUP BY ap.id
HAVING COUNT(DISTINCT s.id) = %s;
"""

# ЗП по региону пока что передаем в аргументе
current_exp_query = """
SELECT ap.name, ap.phone, ap.email
FROM cv
JOIN applicant ap ON cv.applicant_id = ap.id
JOIN experience_view exp ON exp.cv_id = cv.id
WHERE exp.effective_date::date = CURRENT_DATE
  AND EXTRACT(YEAR FROM AGE(exp.effective_date, exp.start_date)) >= 2
  AND cv.salary > %s;
"""

major_in_five_years_query = """
SELECT ap.name, ap.phone, ap.email
FROM cv
JOIN applicant ap ON cv.applicant_id = ap.id
JOIN education edu ON edu.cv_id = cv.id
JOIN experience_view exp ON exp.cv_id = cv.id
JOIN cv_skill ON cv.id = cv_skill.cv_id
JOIN skill s ON s.id = cv_skill.skill_id
WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, edu.end_date)) <= 5
AND edu.major = %s;
"""

like_succesfull_query = """
WITH successful_employee AS (
    SELECT cv.id AS cv_id, a.id AS applicant_id, a.city
    FROM cv
    JOIN applicant a ON cv.applicant_id = a.id
    JOIN progress p ON p.cv_id = cv.id
    WHERE p.status = 'принят' 
      AND a.name = %s 
      AND a.phone = %s
    LIMIT 1
),
skills_match AS (
    SELECT cs.cv_id, COUNT(*) AS skill_score
    FROM cv_skill cs
    WHERE cs.skill_id IN (
        SELECT skill_id FROM cv_skill WHERE cv_id = (SELECT cv_id FROM successful_employee)
    )
    GROUP BY cs.cv_id
),
experience_match AS (
    SELECT e.cv_id, COUNT(*) AS exp_score
    FROM experience e
    WHERE e.category IN (
        SELECT category FROM experience WHERE cv_id = (SELECT cv_id FROM successful_employee)
    )
    GROUP BY e.cv_id
),
city_match AS (
    SELECT cv.id AS cv_id, 1 AS city_score
    FROM cv
    JOIN applicant a ON cv.applicant_id = a.id
    WHERE a.city = (SELECT city FROM successful_employee)
)
SELECT cv.id AS cv_id,
       a.name,
       a.city,
       COALESCE(skills_match.skill_score, 0) +
       COALESCE(experience_match.exp_score, 0) +
       COALESCE(city_match.city_score, 0) AS similarity_score
FROM cv
JOIN applicant a ON cv.applicant_id = a.id
LEFT JOIN skills_match ON cv.id = skills_match.cv_id
LEFT JOIN experience_match ON cv.id = experience_match.cv_id
LEFT JOIN city_match ON cv.id = city_match.cv_id
LEFT JOIN progress p ON cv.id = p.cv_id
WHERE COALESCE(p.status, '') NOT IN ('принят', 'отклонен') -- исключаем только явных
  AND cv.id <> (SELECT cv_id FROM successful_employee)     -- не сравниваем самого успешного
ORDER BY similarity_score DESC, a.name;

"""

