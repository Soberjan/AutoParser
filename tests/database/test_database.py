import pytest
import psycopg2

import testing_entries
from tests.database.database_fixture import database

def test_dump_to_bd(database):
    database.dump_to_db(testing_entries.persons[0])
    
    database.cur.execute("""
                SELECT name, phone, email, city, birth_date
                FROM testing.applicant
                WHERE name = 'Григорьев Иван Андреевич'
                """)

    s = database.cur.fetchone()
    assert s[0] == 'Григорьев Иван Андреевич'
    assert s[1] == '+7 (916) 777-88-99'
    assert s[2] == 'ivan.grig.marketing@yandex.ru'
    assert s[3] == 'Калининград'
    assert s[4] == '08.09.1990'

    database.cur.execute("""
                SELECT id
                FROM testing.applicant
                WHERE name = 'Григорьев Иван Андреевич'
                """)
    applicant_id = database.cur.fetchone()[0]
    
    database.cur.execute(f"""
                SELECT salary
                FROM testing.cv
                WHERE applicant_id = \'{applicant_id}\'
                """)
    s = database.cur.fetchone()
    assert s[0] == 94000.
