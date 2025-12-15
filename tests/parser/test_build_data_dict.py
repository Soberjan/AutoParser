from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise
import os

import pytest

from helpers import case_names

from src.parser.parser import Parser
from reader.docx_reader import DOCXReader
from reader.pdf_reader import PDFReader
from _fixtures import new_doc_parser

DataDictTestCase = NamedTuple(
    "doc_test",
    [("path_to_file", str),
     ("result", dict),
     ("expectation", ContextManager),
     ("name", str)],
)
DataDictTestCases = [
    DataDictTestCase(path_to_file="tests/test_data/documents_tests/Васильев Дмитрий Андреевич.docx",
                     result={"Имя": 'Васильев Дмитрий Андреевич',
                             "Телефон": '+7 (904) 567-89-01',
                             "Email": 'd.vasiliev@email.com',
                             "Город": 'Казань',
                             "Дата рождения": '18.09.1985',
                             "Вакансия": 'Ведущий инженер-проектировщик',
                             "Зарплата": '120 000',
                             "Опыт": 'ООО "ПроектСтрой" — Ведущий инженер-проектировщик\nАпрель 2018 — настоящее время\nРазработка проектной документации\nСогласование проектов с заказчиками\nАвторский надзор\nАО "КазаньГипроГор" — Инженер-проектировщик\nМай 2012 — Март 2018\nВыполнение расчетов\nПодготовка чертежей\nРабота с AutoCAD',
                             "Образование": 'Казанский государственный архитектурно-строительный университет\nМагистр, Промышленное и гражданское строительство (2007 — 2012)\nКазанский строительный колледж\nСреднее специальное, Архитектура (2004 — 2007)',
                             "Навыки": 'AutoCAD, Revit\nПроектирование\nРабота с нормативной документацией\nАвторский надзор',
                             "Другое": 'на О себеПрофессионал с инженерным образованием и опытом проектирования более 10 лет. Внимателен к деталям умею работать с чертежами и проектной документацией. Готов к командировкам.Инфа в прочемНевероятно важная'
                             },
                     expectation=does_not_raise(),
                     name="type_1_read"),
    DataDictTestCase(path_to_file="tests/test_data/documents_tests/Григорьев Иван Андреевич.pdf",
                     result={"Имя": 'Григорьев Иван Андреевич',
                             "Телефон": '+7 (916) 777-88-99',
                             "Email": 'ivan.grig.marketing@yandex.ru',
                             "Город": 'Калининград',
                             "Дата рождения": '08.09.1990',
                             "Вакансия": 'Маркетолог (B2B-направление)',
                             "Зарплата": '94 000',
                             "Опыт": 'ООО "ТехноМаркет" — Руководитель отдела B2B-маркетинга \nЯнварь 2019 — настоящее время \n· Разработка стратегий для корпоративного сегмента  \n· Подготовка кейсов и white papers \n· Организация отраслевых мероприятий  \n \nООО "Промышленные Решения" — Маркетолог \nИюль 2015 — Декабрь 2018 \n· Анализ B2B-рынков \n· Поддержка sales-отдела \n· Подготовка тендерной документации',
                             "Образование": 'Балтийский федеральный университет  \nМагистр, Маркетинг (2008 — 2013) \nАкадемия B2B Marketing \nКурс "Стратегии для сложных продаж" (2020)',
                             "Навыки": '· LinkedIn Marketing \n· HubSpot CRM \n· Подготовка коммерческих предложений \n· Анализ NPS \n· Технический копирайтинг',
                             "Другое": 'на    О себе Эксперт по маркетингу для B2B-сегмента с фокусом на сложных технологичных продуктах.  7 лет. К командировкам готов.'
                             },
                     expectation=does_not_raise(),
                     name="type_2_read"),
]


@pytest.mark.parametrize("case", DataDictTestCases, ids=case_names(DataDictTestCases))
def test_set_data_dict(new_doc_parser: Parser, case: DataDictTestCase):
    with case.expectation:
        _, ext = os.path.splitext(case.path_to_file)
        if ext == '.docx':
            reader = DOCXReader()
            file_str = reader.read_file('tests/test_data/documents_tests/Васильев Дмитрий Андреевич.docx')
        elif ext == '.pdf':
            reader = PDFReader()
            file_str = reader.read_file('tests/test_data/documents_tests/Григорьев Иван Андреевич.pdf')
        
        data_dict = new_doc_parser.build_data_dict(file_str)
        assert data_dict == case.result
        # assert new_doc_parser.read_doc(case.path_to_file) == case.result
