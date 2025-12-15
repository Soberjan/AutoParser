from asyncio import sleep
from datetime import date
from typing import List, Tuple

from examples.w9.models.resume import Resume, ResumeItem
from examples.w9.routes.resume.schemas import QResume


class ModelController:
    async def get_objects(self) -> List[Resume]:
        await sleep(20)
        
        return [
            Resume(id=1, name="Resume1", receive_date=date(2024,12,31)),
            Resume(id=11, name="Resume11", receive_date=date(2020,1,1)),
        ]
    async def get_object(self, obj_id) -> ResumeItem|None:
        if obj_id == 1:
            return ResumeItem(
                id=1, 
                name="Resume1", 
                receive_date=date(2024,12,31), 
                description="ddddddddddddd")
        elif obj_id == 11:
            return ResumeItem(
                id=11, name="Resume11", receive_date=date(2020,1,1), 
                description="ddddddddddddd")
        else:
            return None    
    
    async def create_object(self,obj: QResume) -> ResumeItem:
        return ResumeItem(
                id=1, 
                name="Resume3", 
                receive_date=date(2004,2,3), 
                description="ddddddddddnnnnnnddd")
    
    async def update_object(self, obj_id, obj: QResume) -> ResumeItem|None:
        return ResumeItem(
                id=obj_id, 
                name=obj.name, 
                receive_date=obj.receive_date, 
                description=obj.description)
    async def delete_object(self, obj_id) -> Tuple[ResumeItem|None, bool]:
        return (None, True)
        