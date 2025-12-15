import pytest
import psycopg2
import os

from src.database.database import Database

from tests.database.testing_entries import persons

@pytest.fixture
def database(config):
    db = Database()
    db.connect(db_name=config.db_name, host=config.db_host, user=config.db_user, password=config.db_password)

    db.cur.execute("""
                DROP SCHEMA IF EXISTS testing CASCADE;
                CREATE SCHEMA testing;
                """)

    db.cur.execute('SET search_path TO testing;')
    for file in sorted(os.listdir("migrations")):
        with open(os.path.join('migrations/', file), 'r') as query:
            db.cur.execute(query.read())
    db.conn.commit()
    
    yield db
    
    # db.cur.execute("""
    #             DROP SCHEMA testing CASCADE;
    #             CREATE SCHEMA testing;
    #             """)
    db.conn.commit()
    db.conn.close()

@pytest.fixture
def filled_db(database):
    b2b_id = database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['Маркетолог (B2B-направление)', 'маркетинг', 20000., 'открыта', 'Москва', '2025-01-22', None, '2025-12-22'],
                         ['vacancy'])
    
    python_id = database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['Разработчик Python', 'it', 10000., 'открыта', 'Москва', '2025-01-22', None, '2025-12-22'],
                         ['vacancy'])

    hr_id = database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['HR-менеджер', 'hr', 30000., 'открыта', 'Москва', '2025-01-22', None, '2025-12-22'],
                         ['vacancy'])
    
    manager_id = database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['Менеджер по продажам', 'маркетинг', 40000., 'открыта', 'Москва', '2025-02-22', None, '2025-03-22'],
                         ['vacancy'])
    
    ui_id = database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['UI/UX дизайнер', 'it', 20000., 'закрыта', 'Казань', '2025-01-22', '2025-02-11', '2025-12-22'],
                         ['vacancy'])
    
    database.insert_entry('vacancy',
                         ['vacancy', 'category', 'salary', 'status', 'region', 'opened_at', 'closed_at', 'deadline_date'],
                         ['closed_1', 'it', 10000., 'закрыта', 'Казань', '2025-01-22', '2025-07-11', '2025-12-22'],
                         ['vacancy'])
    
    skills_b2b = ['LinkedIn Marketing', 'HubSpot CRM', 'Анализ NPS']
    for skill in skills_b2b:
        skill_id = database.insert_entry('skill',
                              ['name'],
                              [skill],
                              ['name'])
        
        database.insert_entry('vacancy_skill',
                              ['vacancy_id', 'skill_id'],
                              [b2b_id, skill_id],
                              ['vacancy_id', 'skill_id'],)
        
    skills_python = ['Python', 'SQL']
    for skill in skills_python:
        skill_id = database.insert_entry('skill',
                              ['name'],
                              [skill],
                              ['name'])
        database.insert_entry('vacancy_skill',
                              ['vacancy_id', 'skill_id'],
                              [python_id, skill_id],
                              ['vacancy_id', 'skill_id'],)
    
    skills_manager = ['LinkedIn Marketing', 'SQL', 'Подбор персонала', 'Обучение']
    for skill in skills_manager:
        skill_id = database.insert_entry('skill',
                              ['name'],
                              [skill],
                              ['name'])
        database.insert_entry('vacancy_skill',
                              ['vacancy_id', 'skill_id'],
                              [manager_id, skill_id],
                              ['vacancy_id', 'skill_id'],)
    
    skills_hr = ['LinkedIn Marketing', 'CRM', 'B2B продажи', 'Обучение']
    for skill in skills_hr:
        skill_id = database.insert_entry('skill',
                              ['name'],
                              [skill],
                              ['name'])
        database.insert_entry('vacancy_skill',
                              ['vacancy_id', 'skill_id'],
                              [hr_id, skill_id],
                              ['vacancy_id', 'skill_id'],)

    skills_ui = ['Figma', 'Photoshop', 'Illustrator', 'UX Research']
    for skill in skills_ui:
        skill_id = database.insert_entry('skill',
                              ['name'],
                              [skill],
                              ['name'])
        database.insert_entry('vacancy_skill',
                              ['vacancy_id', 'skill_id'],
                              [ui_id, skill_id],
                              ['vacancy_id', 'skill_id'],)                      
    
    for data_dict in persons:
        database.dump_to_db(data_dict)
    return database