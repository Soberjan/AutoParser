from typing import List
from examples.w9.models.t1 import T1
from examples.w9.routes.base_controller import BaseController


class T1Controller(BaseController):
    async def get_objects(self)->List[T1]|None:
        return await self._dm.get_objects(T1)
    
    async def get_object(self, obj_id:str)->List[T1]|None:
        return await self._dm.get_object(T1, obj_id)