# import pytest
from tests.database.database_fixture import database, filled_db
import src.database.queries.applicant as queries

def test_applicant_queries(filled_db):
    filled_db.cur.execute(queries.experience_category_query, ('it', 3))
    d = filled_db.cur.fetchone()
    assert d[0] == 'Иванов Иван Иванович'
    assert d[1] == '+7 (999) 123-45-67'
    assert d[2] == 'ivanov@example.com'

    filled_db.cur.execute(queries.city_query, ('Калининград',))
    d = filled_db.cur.fetchone()
    assert d[0] == 'Григорьев Иван Андреевич'
    
    filled_db.cur.execute(queries.all_skills_query, (['Python'], 1))
    d = filled_db.cur.fetchone()
    assert d[0] == 'Иванов Иван Иванович'

    filled_db.cur.execute(queries.current_exp_query, (50000.,))
    d = filled_db.cur.fetchone()
    assert d[0] == 'Григорьев Иван Андреевич'
    
    filled_db.cur.execute(queries.major_in_five_years_query, ('Курс "Стратегии для сложных продаж"',))
    d = filled_db.cur.fetchone()
    assert d[0] == 'Григорьев Иван Андреевич'
    
    filled_db.cur.execute(queries.like_succesfull_query, ('Григорьев Иван Андреевич', '+7 (916) 777-88-99'))
    d = filled_db.cur.fetchall()
    assert d[0][1] == 'Алексеев Константин Сергеевич'
    assert d[0][2] == 'Калининград'
    assert d[0][3] == 4
    