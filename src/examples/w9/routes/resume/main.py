
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from examples.w9.models.resume import Resume, ResumeItem
from examples.w9.routes.resume.controller import ModelController
from examples.w9.routes.resume.schemas import QResume


c = ModelController()

router= APIRouter(
    prefix="/stats",
    tags=["Статистика по резюме"],
    responses={404: {"description": "Not found"}}
    )

@router.get(
    "/",
    response_model=List[Resume],
    description="Получить список всех резюме")
async def get_all_resumes()->List[Resume]:
    return await c.get_objects()

@router.get(
    "/{resume_id}",
    response_model=ResumeItem,
    description="Получить описание резюме по id")
async def get_resume(resume_id: int) -> ResumeItem:
    if item:=await c.get_object(resume_id):
        return item
    else:
        raise HTTPException(status_code=404, detail="Resume Not Found")
    
@router.post(
    "/",
    description="Создать резюме")
async def create_resumes(r: QResume = Depends())->ResumeItem:
    return await c.create_object(r)
   
@router.put(
    "/{resume_id}",
    description="Обновить резюме")
async def update_resumes(resume_id:int, r: QResume = Depends()):
    if update_item := await c.update_object(resume_id, r):
        return update_item
    else:
        raise HTTPException(status_code=404, detail="Resume Not Found")    
    
   
@router.delete(
    "/{resume_id}",
    description="Удалить резюме")
async def delete_resumes(resume_id:int):
    deleted_item , finally_del= await c.delete_object(resume_id)
    if deleted_item:
        return deleted_item
    elif finally_del:
        return JSONResponse(content={"detail": f"{resume_id} deleted"})
    else:
        raise HTTPException(status_code=404, detail="Resume Not Found")    
    