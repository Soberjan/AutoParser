from tests.database.database_fixture import database, filled_db
import src.database.queries.analytics as queries

def test_applicant_queries(filled_db):
    filled_db.cur.execute(queries.new_cv_count_query)
    d = filled_db.cur.fetchone()
    assert d[0] == 1

    filled_db.cur.execute(queries.monthly_cvs_query)
    d = filled_db.cur.fetchall()
    assert d[0][1] == 1
    assert d[0][2] == 1
    assert d[1][1] == 6
    assert d[1][2] == 4
    assert d[2][1] == 8
    assert d[2][2] == 1
    
    filled_db.cur.execute(queries.most_candidates_region_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'Москва'
    
    filled_db.cur.execute(queries.popular_skills_query)
    d = filled_db.cur.fetchall()
    assert d[0][0] == 'LinkedIn Marketing'
    assert d[0][1] == 3
    
    
    