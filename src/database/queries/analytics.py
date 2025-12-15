new_cv_count_query = """
SELECT COUNT(DISTINCT cv.id) AS new_cvs_last_week
FROM cv
JOIN progress p ON p.cv_id = cv.id
WHERE p.status = 'подал заявку'
  AND p.start_date >= NOW() - INTERVAL '7 days';
"""

monthly_cvs_query = """
SELECT EXTRACT(YEAR FROM p.start_date) AS year,
       EXTRACT(MONTH FROM p.start_date) AS month,
       COUNT(DISTINCT p.cv_id) AS resumes_submitted
FROM progress p
WHERE p.status = 'подал заявку'
GROUP BY year, month
ORDER BY year, month;
"""

most_candidates_region_query = """
SELECT v.region,
       COUNT(DISTINCT a.id) AS candidates_count
FROM applicant a
JOIN cv ON cv.applicant_id = a.id
JOIN vacancy v ON v.id = cv.vacancy_id
GROUP BY v.region
ORDER BY candidates_count DESC
LIMIT 1;
"""

popular_skills_query = """
SELECT s.name AS skill,
       COUNT(*) AS demand
FROM vacancy v
JOIN vacancy_skill vs ON vs.vacancy_id = v.id
JOIN skill s ON s.id = vs.skill_id
WHERE v.opened_at >= (CURRENT_DATE - INTERVAL '1 year')
  AND (v.closed_at IS NULL OR v.closed_at >= CURRENT_DATE)
GROUP BY s.name
ORDER BY demand DESC;
"""