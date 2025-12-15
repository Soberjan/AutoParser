from fastapi.testclient import TestClient
from tests.database.database_fixture import database, filled_db 
from client_fixture import client 

def test_analytical(client: TestClient):
    data = client.get("/analytics/new_cv_count").json()
    assert data["new_cv_count"] == [[0]]

    data = client.get("/analytics/monthly_cvs").json()
    assert data["monthly_cvs"] == [[2025, 1, 1], [2025, 6, 4], [2025, 9, 1]]

    data = client.get("/analytics/most_candidates_region").json()
    assert data["most_candidates_region"] == [["Москва", 5]]

    data = client.get("/analytics/popular_skills").json()
    assert data["popular_skills"] == [
        ["LinkedIn Marketing", 3],
        ["Обучение", 2],
        ["SQL", 2],
        ["CRM", 1],
        ["Анализ NPS", 1],
        ["HubSpot CRM", 1],
        ["B2B продажи", 1],
        ["Python", 1],
        ["Подбор персонала", 1]
    ]

    data = client.get("/analytics/experience_category?category=it&exp_years=3").json()
    assert data["experience_category"] == [
        ["Иванов Иван Иванович", "+7 (999) 123-45-67", "ivanov@example.com"],
        ["Разраб Два", "+7 (999) 243-11-67", "iva@example.com"]
    ]

    data = client.get("/analytics/city?city=Калининград").json()
    assert data["city"] == [
        ["Григорьев Иван Андреевич", "+7 (916) 777-88-99", "ivan.grig.marketing@yandex.ru"],
        ["Алексеев Константин Сергеевич", "+7 925 777-88-99", "alekseev.konst@gmail.com"]
    ]

    data = client.get("/analytics/all_skills?skills=Python").json()
    assert data["applicants"] == [
        ["Иванов Иван Иванович", "+7 (999) 123-45-67", "ivanov@example.com"],
        ["Разраб Два", "+7 (999) 243-11-67", "iva@example.com"]
    ]

    data = client.get("/analytics/current_exp?min_salary=10").json()
    assert data["current_exp"] == [
        ["Григорьев Иван Андреевич", "+7 (916) 777-88-99", "ivan.grig.marketing@yandex.ru"]
    ]

    data = client.get("/analytics/empty_field_candidate").json()
    assert data["empty_field_candidate"] == [
        [3, "Разраб Два", "+7 (999) 243-11-67", "iva@example.com", 3]
    ]

    data = client.get("/analytics/index_search_example?city=Москва&salary=100").json()
    assert data["index_search_example"] == [
        [2, "Иванов Иван Иванович", "Москва", "ivanov@example.com"],
        [2, "Иванов Иван Иванович", "Москва", "ivanov@example.com"],
        [2, "Иванов Иван Иванович", "Москва", "ivanov@example.com"],
        [3, "Разраб Два", "Москва", "iva@example.com"],
        [3, "Разраб Два", "Москва", "iva@example.com"],
        [3, "Разраб Два", "Москва", "iva@example.com"]
    ]

    data = client.get("/analytics/get_archived_query").json()
    assert data["get_archived_query"] == []

    data = client.get("/analytics/opened_vacancies_query").json()
    assert data["opened_vacancies_query"] == [["Григорьев Иван Андреевич"]]

    data = client.get("/analytics/interview_rejected_query").json()
    assert data["interview_rejected_query"] == [
        [3, "Разраб Два", "+7 (999) 243-11-67", "Москва", 3, "2025-06-23", "2025-06-25"]
    ]

    data = client.get("/analytics/applicant_path_query?name=Иванов Иван Иванович").json()
    assert data["applicant_path_query"] == [["подал заявку"], ["проходит собеседование"]]

    data = client.get("/analytics/avg_time_query").json()
    assert data["avg_time_query"] == [112]

    data = client.get("/analytics/old_cv_query").json()
    assert data["old_cv_query"] == [["Иванов Иван Иванович"]]

    data = client.get("/analytics/opened_vacancies_query").json()
    assert data["opened_vacancies_query"] == [["Григорьев Иван Андреевич"]]

    data = client.get("/analytics/vacancy_category_query?category=hr").json()
    assert data["vacancy_category_query"] == [["HR-менеджер"]]

    data = client.get("/analytics/closed_count_query").json()
    assert data["closed_count_query"] == [[2]]

    data = client.get("/analytics/highest_salary_per_category_query").json()
    assert data["highest_salary_per_category_query"] == [
        [3, "HR-менеджер", "hr", 30000.0, "открыта"],
        [4, "Менеджер по продажам", "маркетинг", 40000.0, "открыта"],
        [5, "UI/UX дизайнер", "it", 20000.0, "закрыта"]
    ]

    data = client.get("/analytics/applicant_count_per_region_query").json()
    assert data["applicant_count_per_region_query"] == [["Москва", 5], ["Казань", 1]]

    data = client.get("/analytics/max_closed_at_query").json()
    assert data["max_closed_at_query"] == [["closed_1", 170], ["UI/UX дизайнер", 20]]
