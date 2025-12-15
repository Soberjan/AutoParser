from tests.database.database_fixture import database, filled_db
import src.database.queries.progress as queries

def test_vacancy_queries(filled_db):
    filled_db.cur.execute(queries.opened_vacancies_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'Григорьев Иван Андреевич'

    filled_db.cur.execute(queries.interview_rejected_query)
    d = filled_db.cur.fetchall()
    assert d[0][1] == 'Разраб Два'
    
    filled_db.cur.execute(queries.applicant_path_query, ('Иванов Иван Иванович',))
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'подал заявку'
    assert d[1][0] == 'проходит собеседование'
    
    filled_db.cur.execute(queries.avg_time_query)
    d = filled_db.cur.fetchall()
    assert int(d[0][0]) == 112

    filled_db.cur.execute(queries.old_cv_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'Иванов Иван Иванович'
