from typing import List, Type

from pydantic import BaseModel
from examples.w4classes.singleton import Config, Singleton
from examples.w6db.database import Database


class DataManager(metaclass=Singleton):
    def __init__(self):
        self._cfg = Config()
        self._db = Database(database="tstbase", host="localhost", user="postgres", password="pgpwd", port=5432)

    @property
    def db(self):
        return self._db
    
    async def get_objects(self, obj_class: Type[BaseModel]) -> List[BaseModel] | None:
        fields = [f for f in obj_class.model_fields.keys()]
        sql = f"select {','.join(fields)} from {obj_class.__name__}"
        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute(sql)
                res = []
                rows = await self.to_dict(cursor)
                for row in rows:
                    res.append(await self._make_model(obj_class, row))
                return res
        except Exception as e:
            self.db.conn.rollback()
            raise e
        
    async def get_object(self, obj_class: Type[BaseModel], item_id: str) -> BaseModel | None:
        fields = [f for f in obj_class.model_fields.keys()]
        sql = f"select {','.join(fields)} from {obj_class.__name__} where id = %s"
        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute(sql, (item_id,))
                rows = await self.to_dict(cursor)
                if len(rows) > 0:
                    return await self._make_model(obj_class, rows[0])
                return None
        except Exception as e:
            self.db.conn.rollback()
            raise e
        
    async def to_dict(self, cursor):
        columns = [desc[0] for desc in cursor.description]
        real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return real_dict
    
    async def _make_model(
            self, obj_class, values
    ):
        if values is None:
            return None
        v = obj_class(**values)
        return v