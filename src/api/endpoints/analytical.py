import datetime
from fastapi import APIRouter, Request, Query
from typing import Annotated, Dict, Optional, List, Tuple
from pydantic import BaseModel

from database.queries import analytics, applicant, optimization, progress, vacancy
from database.database import Database


analytical_router = APIRouter(tags=["Analytics"])
applicant_router = APIRouter(tags=["Applicant"])
optimization_router = APIRouter(tags=["Optimization"])
progress_router = APIRouter(tags=["Progress"])
vacancy_router = APIRouter(tags=["Vacancy"])

def execute_query(db: Database, query: str, params: Tuple[str] = ()):
    db.cur.execute(query, params)
    return db.cur.fetchall()
# ---------------- Pydantic output модели ----------------
class NewCVCountOut(BaseModel):
    new_cv_count: List[List[int]]

class MonthlyCVsOut(BaseModel):
    monthly_cvs: List[List[int]]

class MostCandidatesRegionOut(BaseModel):
    most_candidates_region: List[List[Optional[object]]]

class PopularSkillsOut(BaseModel):
    popular_skills: List[List[Optional[object]]]

class ExperienceCategoryOut(BaseModel):
    experience_category: List[List[str]]

class ExperienceCategoryOut(BaseModel):
    experience_category: List[List[str]]

class CityOut(BaseModel):
    city: List[List[str]]

class AllSkillsOut(BaseModel):
    applicants: List[List[str]]

class CurrentExpOut(BaseModel):
    current_exp: List[List[str]]

class MajorInFiveYearsOut(BaseModel):
    major_in_five_years: List[List[str]]

class LikeSuccessfulOut(BaseModel):
    like_successful: List[List[str]]

class EmptyFieldCandidateOut(BaseModel):
    empty_field_candidate: List[List]

class IndexSearchExampleOut(BaseModel):
    index_search_example: List[List]

class GetArchivedQueryOut(BaseModel):
    get_archived_query: List[List]

class OpenedVacanciesOut(BaseModel):
    opened_vacancies_query: List[List]

class InterviewRejectedOut(BaseModel):
    interview_rejected_query: List[List]

class ApplicantPathOut(BaseModel):
    applicant_path_query: List[List]

class AvgTimeOut(BaseModel):
    avg_time_query: List[int]

class OldCvOut(BaseModel):
    old_cv_query: List[List]

class PastDeadlineOut(BaseModel):
    past_deadline_query: List[List]

class VacancyCategoryOut(BaseModel):
    vacancy_category_query: List[List]

class ClosedCountOut(BaseModel):
    closed_count_query: List[List]

class ManyCandidatesOut(BaseModel):
    many_candidates_query: List[List]

class HighestSalaryPerCategoryOut(BaseModel):
    highest_salary_per_category_query: List[List]

class ApplicantCountPerRegionOut(BaseModel):
    applicant_count_per_region_query: List[List]

class MaxClosedAtOut(BaseModel):
    max_closed_at_query: List[List]

# ---------------- Endpoints ----------------
@analytical_router.get(
    "/analytics/new_cv_count",
    summary="Количество новых резюме",
    description="Возвращает общее количество новых резюме, добавленных в систему.",
    response_model=NewCVCountOut
)
def new_cv_count(request: Request):
    res = execute_query(request.app.state.db, analytics.new_cv_count_query)
    return {"new_cv_count": [[int(x[0])] for x in res]}


@analytical_router.get(
    "/analytics/monthly_cvs",
    summary="Резюме по месяцам",
    description="Возвращает количество резюме, сгруппированных по годам и месяцам.",
    response_model=MonthlyCVsOut
)
def monthly_cvs(request: Request):
    res = execute_query(request.app.state.db, analytics.monthly_cvs_query)
    int_res = [[int(entry[0]), int(entry[1]), int(entry[2])] for entry in res]
    return {"monthly_cvs": int_res}


@analytical_router.get(
    "/analytics/most_candidates_region",
    summary="Регионы с наибольшим количеством кандидатов",
    description="Определяет регионы, в которых зарегистрировано больше всего кандидатов.",
    response_model=MostCandidatesRegionOut
)
def most_candidates_region(request: Request):
    res = execute_query(request.app.state.db, analytics.most_candidates_region_query)
    return {"most_candidates_region": [list(x) for x in res]}


@analytical_router.get(
    "/analytics/popular_skills",
    summary="Популярные навыки",
    description="Возвращает список наиболее часто встречающихся навыков среди кандидатов.",
    response_model=PopularSkillsOut
)
def popular_skills(request: Request):
    res = execute_query(request.app.state.db, analytics.popular_skills_query)
    return {"popular_skills": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/experience_category",
    summary="Кандидаты по категории опыта",
    description="Фильтрация кандидатов по категории и количеству лет опыта.",
    response_model=ExperienceCategoryOut
)
def experience_category(
    category: str = Query(..., description="Категория опыта (например, Junior, Middle, Senior)"),
    exp_years: int = Query(..., description="Количество лет опыта"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.experience_category_query, (category, exp_years))
    return {"experience_category": [list(x) for x in res]}

@applicant_router.get(
    "/analytics/experience_category",
    summary="Кандидаты по категории опыта",
    description="Фильтрация кандидатов по категории и количеству лет опыта.",
    response_model=ExperienceCategoryOut
)
def experience_category(
    category: str = Query(..., description="Категория опыта (например, Junior, Middle, Senior)"),
    exp_years: int = Query(..., description="Количество лет опыта"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.experience_category_query, (category, exp_years))
    return {"experience_category": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/city",
    summary="Кандидаты по городу",
    description="Возвращает список кандидатов, проживающих в указанном городе.",
    response_model=CityOut
)
def city(
    city: str = Query(..., description="Название города"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.city_query, (city,))
    return {"city": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/all_skills",
    summary="Кандидаты по набору навыков",
    description="Фильтрация кандидатов по заданному списку навыков.",
    response_model=AllSkillsOut
)
def all_skills(
    skills: Annotated[List[str] | None, Query(description="Список навыков для фильтрации")] = None,
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.all_skills_query, (skills, len(skills)))
    return {"applicants": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/current_exp",
    summary="Кандидаты с опытом и минимальной зарплатой",
    description="Возвращает кандидатов, чья текущая зарплата превышает заданный минимум.",
    response_model=CurrentExpOut
)
def current_exp(
    min_salary: int = Query(..., description="Минимальная зарплата"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.current_exp_query, (min_salary,))
    return {"current_exp": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/major_in_five_years",
    summary="Кандидаты с прогнозом профессии",
    description="Возвращает кандидатов с указанной специальностью через 5 лет.",
    response_model=MajorInFiveYearsOut
)
def major_in_five_years(
    major: str = Query(..., description="Название профессии"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.major_in_five_years_query, (major,))
    return {"major_in_five_years": [list(x) for x in res]}


@applicant_router.get(
    "/analytics/like_successful",
    summary="Похожие на успешных кандидаты",
    description="Возвращает кандидатов, похожих на успешных по имени и телефону.",
    response_model=LikeSuccessfulOut
)
def like_successful(
    name: str = Query(..., description="Имя кандидата"),
    phone: str = Query(..., description="Телефон кандидата"),
    request: Request = None
):
    res = execute_query(request.app.state.db, applicant.like_succesfull_query, (name, phone))
    return {"like_successful": [list(x) for x in res]}

@optimization_router.get(
    "/analytics/empty_field_candidate",
    summary="Кандидаты с незаполненными полями",
    description="Возвращает список кандидатов, у которых отсутствуют важные данные в резюме.",
    response_model=EmptyFieldCandidateOut
)
def empty_field_candidate(request: Request):
    res = execute_query(request.app.state.db, optimization.empty_field_candidate)
    return {"empty_field_candidate": [list(x) for x in res]}


@optimization_router.get(
    "/analytics/index_search_example",
    summary="Пример поиска с индексом",
    description="Демонстрация работы поискового индекса по городу и зарплате.",
    response_model=IndexSearchExampleOut
)
def index_search_example(
    city: str = Query(..., description="Город для поиска"),
    salary: float = Query(..., description="Минимальная зарплата"),
    request: Request = None
):
    res = execute_query(request.app.state.db, optimization.index_search_example, (city, salary))
    return {"index_search_example": [list(x) for x in res]}


@optimization_router.get(
    "/analytics/get_archived_query",
    summary="Архив вакансий",
    description="Возвращает список архивных вакансий.",
    response_model=GetArchivedQueryOut
)
def get_archived_query(request: Request):
    res = execute_query(request.app.state.db, optimization.get_archived_query)
    return {"get_archived_query": [list(x) for x in res]}

@progress_router.get(
    "/analytics/opened_vacancies_query",
    summary="Открытые вакансии",
    description="Возвращает список всех открытых вакансий.",
    response_model=OpenedVacanciesOut
)
def opened_vacancies_query(request: Request):
    res = execute_query(request.app.state.db, progress.opened_vacancies_query)
    return {"opened_vacancies_query": [list(x) for x in res]}


@progress_router.get(
    "/analytics/interview_rejected_query",
    summary="Отклоненные кандидаты на собеседовании",
    description="Возвращает список кандидатов, которые не прошли собеседование.",
    response_model=InterviewRejectedOut
)
def interview_rejected_query(request: Request):
    res = execute_query(request.app.state.db, progress.interview_rejected_query)
    return {"interview_rejected_query": [list(x) for x in res]}


@progress_router.get(
    "/analytics/applicant_path_query",
    summary="Путь кандидата",
    description="Возвращает последовательность этапов найма, пройденных кандидатом.",
    response_model=ApplicantPathOut
)
def applicant_path_query(
    name: str = Query(..., description="Имя кандидата"),
    request: Request = None
):
    res = execute_query(request.app.state.db, progress.applicant_path_query, (name,))
    return {"applicant_path_query": [list(x) for x in res]}


@progress_router.get(
    "/analytics/avg_time_query",
    summary="Среднее время закрытия вакансии",
    description="Возвращает среднее время (в днях), необходимое для закрытия вакансии.",
    response_model=AvgTimeOut
)
def avg_time_query(request: Request):
    res = execute_query(request.app.state.db, progress.avg_time_query)
    res = [int(entry[0]) for entry in res]
    return {"avg_time_query": res}


@progress_router.get(
    "/analytics/old_cv_query",
    summary="Старые резюме",
    description="Возвращает список резюме, которые давно не обновлялись.",
    response_model=OldCvOut
)
def old_cv_query(request: Request):
    res = execute_query(request.app.state.db, progress.old_cv_query)
    return {"old_cv_query": [list(x) for x in res]}


@progress_router.get(
    "/analytics/past_deadline_query",
    summary="Просроченные вакансии",
    description="Возвращает список вакансий, у которых срок закрытия уже истёк.",
    response_model=PastDeadlineOut
)
def past_deadline_query(request: Request):
    res = execute_query(request.app.state.db, progress.past_deadline_query)
    return {"past_deadline_query": [list(x) for x in res]}

@vacancy_router.get(
    "/analytics/vacancy_category_query",
    summary="Вакансии по категории",
    description="Возвращает список вакансий, относящихся к заданной категории.",
    response_model=VacancyCategoryOut
)
def vacancy_category_query(
    category: str = Query(..., description="Категория вакансии"),
    request: Request = None
):
    res = execute_query(request.app.state.db, vacancy.vacancy_category_query, (category,))
    return {"vacancy_category_query": [list(x) for x in res]}


@vacancy_router.get(
    "/analytics/closed_count_query",
    summary="Количество закрытых вакансий",
    description="Возвращает общее количество вакансий, которые были закрыты.",
    response_model=ClosedCountOut
)
def closed_count_query(request: Request):
    res = execute_query(request.app.state.db, vacancy.closed_count_query)
    return {"closed_count_query": [list(x) for x in res]}


@vacancy_router.get(
    "/analytics/many_candidates_query",
    summary="Вакансии с большим количеством кандидатов",
    description="Возвращает вакансии, на которые подалось больше кандидатов, чем указано в параметре.",
    response_model=ManyCandidatesOut
)
def many_candidates_query(
    candidates_amount: int = Query(..., description="Минимальное количество кандидатов"),
    request: Request = None
):
    res = execute_query(request.app.state.db, vacancy.many_candidates_query, (candidates_amount,))
    return {"many_candidates_query": [list(x) for x in res]}


@vacancy_router.get(
    "/analytics/highest_salary_per_category_query",
    summary="Максимальная зарплата по категориям",
    description="Возвращает максимальные зарплаты для каждой категории вакансий.",
    response_model=HighestSalaryPerCategoryOut
)
def highest_salary_per_category_query(request: Request):
    res = execute_query(request.app.state.db, vacancy.highest_salary_per_category_query)
    return {"highest_salary_per_category_query": [list(x) for x in res]}


@vacancy_router.get(
    "/analytics/applicant_count_per_region_query",
    summary="Количество кандидатов по регионам",
    description="Возвращает количество кандидатов в каждом регионе.",
    response_model=ApplicantCountPerRegionOut
)
def applicant_count_per_region_query(request: Request):
    res = execute_query(request.app.state.db, vacancy.applicant_count_per_region_query)
    return {"applicant_count_per_region_query": [list(x) for x in res]}


@vacancy_router.get(
    "/analytics/max_closed_at_query",
    summary="Последняя дата закрытия вакансии",
    description="Возвращает дату самой поздней закрытой вакансии по регионам или категориям.",
    response_model=MaxClosedAtOut
)
def max_closed_at_query(request: Request):
    res = execute_query(request.app.state.db, vacancy.max_closed_at_query)
    return {"max_closed_at_query": [list(x) for x in res]}