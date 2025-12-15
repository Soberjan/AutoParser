from typing import List
import re
import datetime

import psycopg2
from psycopg2 import sql

from config import Config
from utils.logger import logger

class Database():
    """
    Класс для работы с базой данных
    """
    def connect(self, host : str = Config.db_host, db_name : str = Config.db_name, user : str = Config.db_user, password : str = Config.db_password):
        """
        Подключаемся к базе данных

        Args:
            host(str) : Хост датабазы
            db_name(str) : Имя датабазы
            user(str) : Юзер датабазы
            password(str) : Пароль датабазы
        """
        logger.info(Config.db_host)
        self.conn = psycopg2.connect(f"host={host} dbname={db_name} user={user} password={password}")
        self.cur = self.conn.cursor()
        
    def disconnect(self):
        """
        Отключаемся от базы данных
        """
        self.conn.close()
    
    def insert_entry(self, table : str, columns : List[str], values : List[str], conflict_columns : List[str]):
        """
        Вставить запись в таблицу

        Args:
            table(str) : таблица в которую вставляем запись
            columns(List[str]) : какие колонки вставляем
            values(List[str]) : какие значения вставляем
            conflict_columns(List[str]) : какие колонки проверяем на уникальность
        Returns:
            id(str) : id вставленного поля
        """
        query = sql.SQL("""
            insert into {table} ({columns})
            values ({values})
            on conflict ({conflict})
            do update set {update}
            returning id
            """
            ).format(
                    table=sql.Identifier(table),
                    columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                    values=sql.SQL(', ').join(sql.Placeholder() * len(columns)),
                    conflict=sql.SQL(', ').join(map(sql.Identifier, conflict_columns)),
                    update=sql.SQL(', ').join(
                        sql.Composed([sql.Identifier(col), sql.SQL(" = EXCLUDED."), sql.Identifier(col)])
                        for col in conflict_columns[:1]
                    )
                    )
        self.cur.execute(query, values)
        return self.cur.fetchone()[0]
    
    def to_float(self, s : str):
        return float(s.replace(' ', '').replace(',', '.')) if s else None
    
    def to_date(self, s : str, start = True):
        months = {
            "Январь": "01",
            "Февраль": "02",
            "Март": "03",
            "Апрель": "04",
            "Май": "05",
            "Июнь": "06",
            "Июль": "07",
            "Август": "08",
            "Сентябрь": "09",
            "Октябрь": "10",
            "Ноябрь": "11",
            "Декабрь": "12"
        }
        if s == None:
            return
        
        if m := re.search(r'(настоящее время)', s):
            return '9999-12-31' # флаг настоящего времени, на основе которого строим вью, который динамически сегодняшний день возвращает
        
        if m := re.search(r'(?P<day>\d\d).(?P<month>\d\d).(?P<year>\d\d\d\d)', s):
            d = m.groupdict()
            return f'{d['year']}-{d['month']}-{d['day']}'
        
        if m := re.search(r'(?P<month>[\w]+) (?P<year>\d\d\d\d)', s):
            d = m.groupdict()
            return f'{d['year']}-{months[d['month']]}-01'
        
        if m := re.search(r'(?P<year>\d\d\d\d)', s):
            d = m.groupdict()
            month = '01' if start else '12'
            return f'{d['year']}-{month}-01'
    
    def dump_to_db(self, data_dict : dict):
        """
        Скидываем инфу о соискателе в базу данных

        Args:
            data_dict(dict) : словарь с инфой о соискателе
        """
        applicant_columns = ['name', 'phone', 'email', 'city', 'birth_date']
        applicant_entry = {col: data_dict[col][0][col] for col in applicant_columns if len(data_dict[col]) > 0}
        applicant_id = self.insert_entry('applicant',
                                         applicant_entry.keys(),
                                         list(applicant_entry.values()),
                                         ['name', 'phone'])
        
        if len(data_dict['vacancy']) > 0:
            vacancy_entry = data_dict['vacancy'][0]
            vacancy_id = self.insert_entry('vacancy',
                                            vacancy_entry.keys(),
                                            list(vacancy_entry.values()),
                                            ['vacancy'])
        
        cv_columns = ['salary', 'other']
        data_dict['other'] = [{'other': ''.join([d['other'] for d in data_dict['other']])}]
        cv_entry = {col: data_dict[col][0][col] for col in cv_columns if len(data_dict[col]) > 0}
        cv_entry['applicant_id'] = applicant_id
        cv_entry['vacancy_id'] = vacancy_id
        cv_entry['salary'] = self.to_float(cv_entry.get('salary'))
        cv_id = self.insert_entry('cv',
                                  cv_entry.keys(),
                                  list(cv_entry.values()),
                                  ['applicant_id', 'vacancy_id'])

        experience_entries = data_dict['experience']
        for experience_entry in experience_entries:
            experience_entry['start_date'] = self.to_date(experience_entry.get('start_date'))
            experience_entry['end_date'] = self.to_date(experience_entry.get('end_date'))
            experience_entry['cv_id'] = cv_id
            self.insert_entry('experience',
                            experience_entry.keys(),
                            list(experience_entry.values()),
                            ['company', 'position', 'start_date', 'end_date', 'cv_id'])

        education_entries = data_dict['education']
        for education_entry in education_entries:
            education_entry['start_date'] = self.to_date(education_entry.get('start_date'))
            education_entry['end_date'] = self.to_date(education_entry.get('end_date')) if education_entry.get('end_date') else education_entry['start_date']
            education_entry['end_date'] = self.to_date(education_entry.get('end_date'))
            education_entry['cv_id'] = cv_id
            self.insert_entry('education',
                            education_entry.keys(),
                            list(education_entry.values()),
                            ['institute', 'major', 'degree', 'start_date', 'end_date', 'cv_id'])

        skill_entries = data_dict['skill']
        skill_ids = []
        for skill_entry in skill_entries:
            skill_id = self.insert_entry('skill',
                                         skill_entry.keys(),
                                         list(skill_entry.values()),
                                         ['name'])
            skill_ids.append(skill_id)
        
        for skill_id in skill_ids:
            self.insert_entry('cv_skill',
                              ['cv_id', 'skill_id'],
                              [cv_id, skill_id],
                              ['cv_id', 'skill_id'])
        
        if progress_entries := data_dict.get('progress'):
            for progress_entry in progress_entries:
                    progress_entry['start_date'] = self.to_date(progress_entry.get('start_date'))
                    progress_entry['end_date'] = self.to_date(progress_entry.get('end_date'))
                    progress_entry['cv_id'] = cv_id
                    skill_id = self.insert_entry('progress',
                                    progress_entry.keys(),
                                    list(progress_entry.values()),
                                    ['id'])
        
        
        self.conn.commit()

    def _print_table(self, table_name : str):
        """
        Метод для дебагинга, рисует таблицу из базы данных
        """
        self.cur.execute(
            f"SELECT * FROM {table_name}",
        )
        logger.info(self.cur.fetchall())
    
    def _delete_everything(self):
        """
        Метод для дебагинга, удаляет все данные из всех таблиц
        """
        self.cur.execute("DELETE FROM applicants")
        self.cur.execute("DELETE FROM skills")
        self.cur.execute("DELETE FROM vacancies")
        self.cur.execute("DELETE FROM applicants_to_skills")
        self.cur.execute("DELETE FROM applicants_to_vacancies")