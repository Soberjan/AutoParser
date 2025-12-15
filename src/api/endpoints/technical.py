from fastapi import APIRouter, Request, Query
from typing import List, Optional
from pydantic import BaseModel

from database.queries import technical

technical_router = APIRouter(tags=["Technical"])


# Модели ответов
class CVIdResponse(BaseModel):
    get_cv_ids: List[Optional[int]]


class UpdateStatusResponse(BaseModel):
    update_cv_progress: str


class UpdateVacancyStatusResponse(BaseModel):
    update_vacancy_status: str


class AddVacancyResponse(BaseModel):
    add_vacancy: str


class AddSkillResponse(BaseModel):
    add_skill: str


class AutoreplyResponse(BaseModel):
    autoreply: str


# Модели запросов
class UpdateCVStatusRequest(BaseModel):
    cv_id: int
    status: str


class UpdateVacancyStatusRequest(BaseModel):
    vacancy_id: int
    status: str


class AddVacancyRequest(BaseModel):
    name: str
    category: str
    salary: float
    region: str
    deadline_date: str
    skills: Optional[List[str]] = []


class AddSkillRequest(BaseModel):
    name: str


class AutoreplyRequest(BaseModel):
    email: str
    msg: str


# --- Эндпоинты ---
@technical_router.get(
    "/technical/get_cv_ids",
    summary="Получить ID резюме",
    description="Возвращает список идентификаторов резюме по имени и телефону кандидата.",
    response_model=CVIdResponse
)
def get_cv_ids(
    name: str = Query(..., description="Имя кандидата"),
    phone: str = Query(..., description="Телефон кандидата"),
    request: Request = None
):
    db = request.app.state.db
    db.cur.execute(technical.get_cv_ids, (name, phone))
    res = db.cur.fetchall()
    ids = [row[0] for row in res]
    return CVIdResponse(get_cv_ids=ids)


@technical_router.post(
    "/technical/update_cv_status",
    summary="Обновить статус резюме",
    description="Изменяет статус резюме по его ID.",
    response_model=UpdateStatusResponse
)
def update_cv_status(body: UpdateCVStatusRequest, request: Request):
    db = request.app.state.db
    
    db.cur.execute(technical.close_cv_status, (body.cv_id,))
    if db.cur.rowcount == 0:
        return UpdateStatusResponse(update_cv_progress="cv_id doesn't exist or already archived")
    
    try:
        db.cur.execute(technical.new_cv_status, (body.cv_id, body.status))
    except Exception as e:
        return UpdateStatusResponse(update_cv_progress=f"error {e}")
    
    db.conn.commit()
    return UpdateStatusResponse(update_cv_progress="succesfully updated status")


@technical_router.post(
    "/technical/update_vacancy_status",
    summary="Обновить статус вакансии",
    description="Изменяет статус вакансии по ее ID.",
    response_model=UpdateVacancyStatusResponse
)
def update_vacancy_status(body: UpdateVacancyStatusRequest, request: Request):
    db = request.app.state.db
    
    db.cur.execute(technical.update_vacancy_status, (body.status, body.vacancy_id))
    if db.cur.rowcount == 0:
        return UpdateVacancyStatusResponse(update_vacancy_status="vacancy_id doesn't exist or already archived")
    db.conn.commit()
    
    return UpdateVacancyStatusResponse(update_vacancy_status="succesfully updated status")


@technical_router.post(
    "/technical/add_vacancy",
    summary="Добавить вакансию",
    description="Создает новую вакансию с заданными параметрами и привязывает к ней навыки.",
    response_model=AddVacancyResponse
)
def add_vacancy(body: AddVacancyRequest, request: Request):
    db = request.app.state.db
    
    try:
        db.cur.execute(technical.add_vacancy, (body.name, body.category, body.salary, body.region, body.deadline_date))
        vacancy_id = db.cur.fetchone()[0]
        for skill in body.skills:
            db.cur.execute(technical.skill_id, (skill,))
            res = db.cur.fetchone()
            if res:
                skill_id = res[0]
                db.cur.execute(technical.add_vacancy_skill, (vacancy_id, skill_id))
    except Exception as e:
        return AddVacancyResponse(add_vacancy=f"error {e}")
    
    db.conn.commit()
    return AddVacancyResponse(add_vacancy=str(vacancy_id))


@technical_router.post(
    "/technical/add_skill",
    summary="Добавить новый навык",
    description="Добавляет новый навык в базу данных.",
    response_model=AddSkillResponse
)
def add_skill(body: AddSkillRequest, request: Request):
    db = request.app.state.db
    
    try:
        db.cur.execute(technical.add_skill, (body.name,))
    except Exception as e:
        return AddSkillResponse(add_skill=f"error {e}")
    
    db.conn.commit()
    return AddSkillResponse(add_skill="succesfully added skill")


@technical_router.post(
    "/technical/autoreply",
    summary="Автоответ по email",
    description="Отправляет письмо кандидату с заданным сообщением.",
    response_model=AutoreplyResponse
)
def autoreply(body: AutoreplyRequest, request: Request):
    sender = request.app.state.sender
    
    try:
        sender.send_msg(body.email, "Устройство на работу", body.msg)
    except Exception as e:
        return AutoreplyResponse(autoreply=f"error {e}")
    
    return AutoreplyResponse(autoreply="Succesfully sent a message")
