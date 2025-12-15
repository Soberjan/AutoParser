opened_vacancies_query = """
SELECT a.name
FROM progress p
JOIN cv ON p.cv_id = cv.id
JOIN applicant a ON cv.applicant_id = a.id
WHERE p.status = 'проходит собеседование' and EXTRACT(MONTH FROM p.end_date) = EXTRACT(MONTH FROM CURRENT_DATE)
"""

interview_rejected_query = """
SELECT a.id AS applicant_id,
       a.name,
       a.phone,
       a.city,
       cv.id AS cv_id,
       p1.start_date AS interview_date,
       p2.start_date AS rejection_date
FROM applicant a
JOIN cv ON cv.applicant_id = a.id
JOIN progress p1 ON p1.cv_id = cv.id AND p1.status = 'проходит собеседование'
JOIN progress p2 ON p2.cv_id = cv.id AND p2.status = 'отклонен'
"""

applicant_path_query = """
SELECT p.status
FROM progress p
JOIN cv ON p.cv_id = cv.id
JOIN applicant a ON cv.applicant_id = a.id
WHERE a.name = %s
"""

avg_time_query = """
SELECT AVG(p_prinyat.start_date - p_zayavka.start_date) AS avg_days_to_hire
FROM cv
JOIN progress p_zayavka 
    ON p_zayavka.cv_id = cv.id AND p_zayavka.status = 'подал заявку'
JOIN progress p_prinyat 
    ON p_prinyat.cv_id = cv.id AND p_prinyat.status = 'принят';
"""

old_cv_query = """
SELECT a.name
FROM progress p
JOIN cv ON p.cv_id = cv.id
JOIN applicant a ON cv.applicant_id = a.id
WHERE p.status = 'проходит собеседование'
AND p.end_date IS NULL AND  EXTRACT(MONTH FROM AGE(CURRENT_DATE, p.start_date)) > 6
"""
