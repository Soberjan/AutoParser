from urllib.parse import urlencode

from tests.database.database_fixture import database, filled_db 
from tests.api.endpoints.client_fixture import client 
import src.database.queries.progress as progress

def test_technical(client):
    # делаем это чтобы в запросе нормально передать номер телефона
    params = {
        "name": "Иванов Иван Иванович",
        "phone": "+7 (999) 123-45-67"
    }
    query_string = urlencode(params)
    data = client.get(f"/technical/get_cv_ids?{query_string}").json()
    assert data['get_cv_ids'][0] == 2

    # теперь тело запроса через JSON
    data = client.post(
        "/technical/update_cv_status",
        json={"cv_id": 2, "status": "отклонен"}
    ).json()
    assert data['update_cv_progress'] == "succesfully updated status"

    data = client.get(
        "/analytics/applicant_path_query?name=Иванов Иван Иванович"
    ).json()
    assert data['applicant_path_query'] == [["подал заявку"], ["проходит собеседование"], ["отклонен"]]

    data = client.post(
        "/technical/add_vacancy",
        json={
            "name": "Вакансия",
            "category": "it",
            "salary": 100,
            "region": "Москва",
            "deadline_date": "2025-12-25",
            "skills": ["Linux", "SQL"]
        }
    ).json()
    assert data['add_vacancy'] == '13'

    data = client.post(
        "/technical/update_vacancy_status",
        json={"vacancy_id": 13, "status": "закрыта"}
    ).json()
    assert data['update_vacancy_status'] == "succesfully updated status"

    data = client.post(
        "/technical/add_skill",
        json={"name": "igra_rulem_na_royale"}
    ).json()
    assert data['add_skill'] == "succesfully added skill"
