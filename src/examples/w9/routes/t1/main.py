from typing import List
from examples.w9.models.t1 import T1
from examples.w9.routes.t1.controller import T1Controller

from fastapi import APIRouter, HTTPException

c = T1Controller()

router= APIRouter(
    prefix="/t1",
    tags=["t1 information"],
    responses={404: {"description": "Not found"}}
    )

@router.get(
    "/",
    response_model=List[T1],
    description="Получить список всех t1")
async def get_all_t1()->List[T1]:
    return await c.get_objects()

@router.get(
    "/{obj_id}",
    response_model=T1,
    description="Получить описание t1 по id")
async def get_t1(obj_id: str) -> T1:
    if item:=await c.get_object(obj_id):
        return item
    else:
        raise HTTPException(status_code=404, detail="T1 not found")

