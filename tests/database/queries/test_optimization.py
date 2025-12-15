# import pytest
from tests.database.database_fixture import database, filled_db
import src.database.queries.optimization as queries

def test_optimization_queries(filled_db):
    filled_db.cur.execute(queries.empty_field_candidate)
    d = filled_db.cur.fetchone()
    assert d[1] == 'Разраб Два'
    assert d[2] == '+7 (999) 243-11-67'
    
    filled_db.cur.execute(queries.index_search_example, ('Москва', 100.))
    d = filled_db.cur.fetchone()
    assert d[1] == 'Иванов Иван Иванович'
    assert d[2] == 'Москва'
    
    filled_db.cur.execute(queries.archive_query)
    filled_db.cur.execute(queries.get_archived_query)
    d = filled_db.cur.fetchone()
    assert d[2] == 'Иванов Иван Иванович'