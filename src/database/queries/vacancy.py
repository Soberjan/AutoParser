opened_vacancies_query = """
SELECT v.vacancy
FROM vacancy v
WHERE v.status = 'открыта'
"""

past_deadline_query = """
SELECT v.vacancy
FROM vacancy v
WHERE CURRENT_DATE > v.deadline_date
"""

vacancy_category_query = """
SELECT v.vacancy
FROM vacancy v
WHERE v.category = %s
"""

closed_count_query = """
SELECT COUNT(*)
FROM vacancy v
WHERE v.status = 'закрыта' AND EXTRACT(YEAR FROM CURRENT_DATE) = EXTRACT(YEAR FROM v.closed_at) 
"""

many_candidates_query = """
SELECT v.id, v.vacancy, COUNT(DISTINCT cv.applicant_id) AS candidate_count
FROM vacancy v
JOIN cv ON v.id = cv.vacancy_id
GROUP BY v.id, v.vacancy
HAVING COUNT(DISTINCT cv.applicant_id) > %s
ORDER BY candidate_count DESC;
"""

highest_salary_per_category_query = """
SELECT v.id,
       v.vacancy,
       v.category,
       v.salary,
       v.status
FROM vacancy v
WHERE v.salary = (
    SELECT MAX(v2.salary)
    FROM vacancy v2
    WHERE v2.category = v.category
);
"""

applicant_count_per_region_query = """
SELECT v.region, COUNT(DISTINCT cv.applicant_id) AS candidate_count
FROM vacancy v
JOIN cv ON v.id = cv.vacancy_id
GROUP BY v.region
ORDER BY candidate_count DESC;
"""

# Пока что вакансия которая дольше всего закрывается, потому что сразу не сделал таблицу так, чтобы у одной вакансии несколько инстансов было -_-
max_closed_at_query = """
SELECT v.vacancy, v.closed_at - v.opened_at AS duration_days
FROM vacancy v
WHERE v.closed_at IS NOT NULL
ORDER BY duration_days DESC;
"""
