CREATE VIEW experience_view AS
SELECT e.*,
       CASE 
           WHEN e.end_date = '9999-12-31'::date THEN CURRENT_DATE
           ELSE e.end_date
       END AS effective_date
FROM experience e;

CREATE VIEW education_view AS
SELECT e.*,
       CASE
           WHEN e.end_date = '9999-12-31'::date THEN CURRENT_DATE
           ELSE e.end_date
       END AS effective_date
FROM education e;
