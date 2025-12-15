# import pytest
from tests.database.database_fixture import database, filled_db
import src.database.queries.vacancy as queries

def test_vacancy_queries(filled_db):
    filled_db.cur.execute(queries.opened_vacancies_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'Маркетолог (B2B-направление)'
    assert d[1][0] == 'Разработчик Python'
    assert d[2][0] == 'HR-менеджер'
    assert d[3][0] == 'Менеджер по продажам'

    filled_db.cur.execute(queries.past_deadline_query)
    d = filled_db.cur.fetchone()
    assert d[0] == 'Менеджер по продажам'
    
    filled_db.cur.execute(queries.vacancy_category_query, ('hr',))
    d = filled_db.cur.fetchone()
    assert d[0] == 'HR-менеджер'
    
    filled_db.cur.execute(queries.closed_count_query)
    d = filled_db.cur.fetchone()
    assert d[0] == 2
    
    filled_db.cur.execute(queries.many_candidates_query, (1,))
    d = filled_db.cur.fetchall()
    assert d[0][1] == 'Разработчик Python'

    filled_db.cur.execute(queries.highest_salary_per_category_query)
    d = filled_db.cur.fetchall()
    assert d[0][1] == 'HR-менеджер'
    assert d[0][2] == 'hr'
    assert d[0][3] == 30000.

    filled_db.cur.execute(queries.applicant_count_per_region_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'Москва'
    assert d[0][1] == 5
    assert d[1][0] == 'Казань'
    assert d[1][1] == 1
    
    filled_db.cur.execute(queries.max_closed_at_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'closed_1'
    assert d[0][1] == 170
    

