import os
import re
import shutil
import time
from typing import NamedTuple, List, Dict

from utils.logger import logger
from utils.decorators import timer
from config import Config
from database.database import Database
import utils.enums as enums
from fetcher.fetcher import Fetcher



class ReInfo(NamedTuple):
    """
    Вспомогательный класс для организации информации об искомых полях
    """
    templates : List[str]
    block : str = r'(?P<content>[\s\S]*)'
    all_entries : bool = False

class Parser:
    """
    Класс для парсинга резюме из документов формата .docx и .pdf
    """
    _regex_dict = {
        "name" : ReInfo(templates=[r'(?P<name>\b[А-ЯЁ][а-яё]*[ .]+?[А-ЯЁ][а-яё]*[ .]+[А-ЯЁ]*[а-яё]*\b)',
                                r'(?P<name>\b[А-ЯЁ][а-яё]*[ .]+?[А-ЯЁ][а-яё]*\b)'
                            ]),
        "phone" : ReInfo(templates=[r'(?P<phone>\+?\d+ ?\(?\d\d\d\)? ?\d\d\d[ -]*\d\d[ -]*\d\d)']),
        "email" :ReInfo(templates=[r'(?P<email>\b[\w.]*\@\w*.\w*\b)']),
        "city" : ReInfo(templates=[r'(?:Город\:|Гор\.|\bгор\.|\bгор\:?)\s*(?P<city>[\w \-]*)']),
        "birth_date" : ReInfo(templates=[r'Дата рождения:? ?(?P<birth_date>\d\d.?\d\d.?\d\d\d\d)']),
        "salary" : ReInfo(templates=[r'(?P<salary>[\d .]*)?рублей']),
        "other" : ReInfo(templates=[r'Цель[ :$]*(?P<other>[\s\S]*?)(Достижения|Опыт работы|Навыки|Дополнительная информация|О себе|\Z)',
                            r'О себе[ :$]*(?P<other>[\s\S]*?)(Достижения|Опыт работы|Навыки|Дополнительная информация|Цель|\Z)',
                            r'Дополнительная информация[ :$]*(?P<other>[\s\S]*?)(Достижения|Опыт работы|Навыки|О себе|Цель|\Z)'],
                            all_entries=True),
        "vacancy" : ReInfo(templates=[r'(Должность[\:\s]*|Вакансия[:\s]*)(?P<vacancy>[ \(\)\d\/\-\w]*)']),
        "experience":
            ReInfo(templates=[r'(?P<company>[\w \-\"\(\)]*) — (?P<position>[\w \-\"\(\)]*)\n(?P<start_year>[\d\w ]*) — (?P<end_year>[\d\w ]*)',
                            r'(?P<company>[\w \-\"\(\)]*)\n(?P<position>[\w \-\"\(\)]*)\n(?P<start_year>[\d\w ]*) — (?P<end_year>[\d\w ]*)',
                            r'(?P<position>[\w \-\"\(\)]*)\n(?P<company>[\w \-\"\(\)]*),[ \w]*\n(?P<start_year>[\d\w ]*) — (?P<end_year>[\d\w ]*)',
                            r'(?P<position>[\w \-\"\(\)]*)\n(?P<company>[\w \-\"\(\)]*),(?P<start_year>[\d\w ]*)\–(?P<end_year>[\d\w ]*)'
                            ], 
                block=r'Опыт работы[ :]*(?P<content>[\s\S]*?)(Достижения|Образование|Навыки|Дополнительная информация|О себе|\Z)',
                all_entries=True),
        "education": 
            ReInfo(templates=[r'(?P<institute>[\w \-\"\(\)\,]*)\n(?P<degree>[\w \-]*), (?P<major>[\w \-\"]*) \((?P<start_year>[\d]*) — (?P<end_year>[\d]*)\)',
                            r'(?P<institute>[\w \-\"\(\)\,]*)\n(?P<degree>[\w \-]*), (?P<major>[\w \-\"]*)\n(?P<start_year>[\d]*) — (?P<end_year>[\d]*)',
                            r'(?P<institute>[\w \-\"\(\)\,]*)\n(?P<major>[\w \-\"]*)\((?P<start_year>[\d]*)\)',
                            r'(?P<major>[\w \-\"]*)\n(?P<institute>[\w \-\"\(\)\,]*)\, (?P<start_year>[\d]*)\–(?P<end_year>[\d]*)',
                            r'(?P<institute>[\w \-\"\(\)\,]*)\n(?P<end_year>[\d]*) г\.',
                            ],
                block=r'Образование[ :$]*(?P<content>[\s\S]*?)(Достижения|Опыт работы|Навыки|Дополнительная информация|О себе|\Z)',
                all_entries=True),
        "skill":
            ReInfo(templates=[r'[·•]*(?P<name>[\w\.\/\(\) \-—\:]*)(\n|, )'], 
                block=r'Навыки[ :$]*(?P<content>[\s\S]*?)(Достижения|Опыт работы|Образование|Дополнительная информация|О себе|\Z)',
                all_entries=True),
    }
    
    def __init__(self, db : Database):
        self.db = db
    
    def extract_re_info(self, re_info : ReInfo, source: str) -> List[Dict[str, str]]:
        """Вытащить из строки source строку, которая подходит под данные, указанные в re_info

        Args:
            re_info(ReInfo) : информация об искомом поле в виде набора регулярных выражений
            source(str) : строка в которой ищем подстроку
        """
        if not (block := re.search(re_info.block, source)):
            return 
        block = block['content'].strip()
        
        if re_info.all_entries:
            return [
                m.groupdict()
                for t in re_info.templates
                for m in re.finditer(t, block)
            ]

        for t in re_info.templates:
            m = re.search(t, block)
            if m:
                return [m.groupdict()]
        return []

    def build_data_dict(self, data_str: str) -> dict:
        """Выгрузить необходимые данные из строки в словарь. Если данных нет, значение - ''

        Args:
            data_str(str) : входные данные
        Returns:
            dict : словарь с данными
        """

        d = {attribute : self.extract_re_info(re_info, data_str) for attribute, re_info in self._regex_dict.items()}
        return d
    
    @timer
    def parse(self, text : str, mode : str = 'db'):
        """
        Обработать строку text
        
        Args:
            text(str) : текст для парсинга
            mode(str) : режим, в котором сохраняем аутпут. db - дефолтный, сохраняем в базу данных, file - сохраняем в файл в директорию Config.parser_output_path 
        """
        data_dict = self.build_data_dict(text)
        
        if mode == 'db':
            self.db.dump_to_db(data_dict)
        elif mode == 'file':
            self.save_to_md(data_dict)
        else:
            logger.error('Неподдерживаемый режим, поддерживаемые режим - file и db')
    
    def parse_dir(self, dir : str, mode : str = 'db'):
        """
        Обработать все файлы из директории dir
        
        Args:
            text(str) : директория из которой берем файлы
            mode(str) : режим, в котором сохраняем аутпут. db - дефолтный, сохраняем в базу данных, file - сохраняем в файл в директорию Config.parser_output_path 
        """
        for file in os.listdir(dir):
            _, ext = os.path.splitext(file)
            file_type = enums.FileTypes(ext)
            logger.info('Обрабатываю ' + file)
            if file_type != enums.FileTypes.UNKNOWN:
                reader = enums.READERS[file_type]
                text = reader.read_file(os.path.join(Config.parser_input_path, file))
                self.parse(text, mode)
                logger.info('Обработанный файл ' + file)
                logger.info(f'Сохранен в режиме {mode}')
    
    def parse_fetcher(self, fetcher : Fetcher, new : bool):
        """
        Обработать все файлы из источника данных
        
        Args:
            fetcher(Fetcher) : источник данных
            new(bool) : если true, скачиваем только новые файлы, иначе - все
        """
        dir_name = os.path.join(os.path.curdir, '/tmp')
        os.mkdir(dir_name)
        fetcher.download_files(new, dir_name)
        self.parse_dir(dir_name)
        shutil.rmtree(dir_name)    
    
    def listen_fetcher(self, fetcher : Fetcher):
        """
        Прослушивает источник данных, если в нем появились новые файлы - обрабатыавет их
        
        Args:
            fetcher(Fetcher) : источник данных
        """
        while True:
            self.parse_fetcher(fetcher, True)
            time.sleep(10)
    
    def save_to_md(self, data_dict : dict, output_dir : str = Config.parser_output_path):
        """Сохранить словарь в markdown файл

        Args:
            data_dict(dict) : словарь с данными
            filename(str) : файл в который сохраняем
        Returns:
            dict : словарь с данными
        """
        output_dir = Config.parser_output_path
        output_file_name = data_dict['Имя'] + '.md'
        output_path = os.path.join(output_dir, output_file_name)
            
        markdown_content = ''
        for key, value in data_dict.items():
            markdown_content += key + ' ' + value + '\n'

        with open(output_path, "w") as f:
            f.write(markdown_content)