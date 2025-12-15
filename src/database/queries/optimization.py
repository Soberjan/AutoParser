# Проверить наличие дубликатов резюме (по email или номеру телефона).
# Сделано в самой таблице: CONSTRAINT unique_applicant_vacancy UNIQUE (applicant_id, vacancy_id)

empty_field_candidate = """
SELECT DISTINCT a.id AS applicant_id,
       a.name,
       a.phone,
       a.email,
       cv.id AS cv_id
FROM applicant a
JOIN cv ON cv.applicant_id = a.id
LEFT JOIN education e ON e.cv_id = cv.id
LEFT JOIN experience ex ON ex.cv_id = cv.id
WHERE e.id IS NULL OR ex.id IS NULL;
"""

# Для примера делаю поиск с индексами, мб позже вдумчивее реализую
index_search_example = """
SELECT a.id, a.name, a.city, a.email
FROM applicant a
JOIN cv ON cv.applicant_id = a.id
JOIN cv_skill cs ON cs.cv_id = cv.id
JOIN skill s ON s.id = cs.skill_id
WHERE a.city = %s
  AND cv.salary >= %s
"""

# Проверить, что все вакансии имеют корректные даты (дата закрытия не раньше даты открытия).
# Сделано в бд с помощью констрэйнта

archive_query = """
UPDATE progress
SET status = 'архивирован'
WHERE (
        (end_date IS NULL AND start_date <= CURRENT_DATE - INTERVAL '6 months')
        OR
        (end_date IS NOT NULL AND end_date <= CURRENT_DATE - INTERVAL '6 months')
      )
  AND status <> 'архивирован';  -- чтобы не трогать уже архивированные
"""

get_archived_query = """
SELECT cv.id AS cv_id,
       a.id AS applicant_id,
       a.name,
       a.phone,
       a.email,
       p.status,
       p.start_date,
       p.end_date
FROM cv
JOIN applicant a ON a.id = cv.applicant_id
JOIN progress p ON p.cv_id = cv.id
WHERE p.status = 'архивирован';
"""

# Построить запрос для синхронизации данных между таблицами (например, обновление статуса вакансии после найма кандидата).
# Буду по контексту смотреть, где нужно это делать, когда появятся эндпойнты