import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({'TESTING': True, })
    yield app


@pytest.fixture()
def client_create(app):
    return app.test_client()


@pytest.fixture()
def client_work(app):
    return app.test_cli_runner()


def test_parametrs_on_bd(client_create):
    """Отправляем данные в теле запроса которые точно есть в БД"""
    response = client_create.post("/get_form", data={
        "email_var_1_1": 'email', "phone_var_1_2": "phone"
    })

    assert response.status_code == 200


def test_parametrs_on_validate_form(client_create):
    """Отправляем данные в теле запроса которые точно есть в БД"""
    response = client_create.post("/get_form", data={
        "date": '12.12.2025', "phone": "7 909 878 98 89", 'email': 'gbdf@mail.ru'
    })

    assert response.status_code == 200


def test_parametrs_no_validate_form(client_create):
    """Отправляем данные в теле запроса которые точно есть в БД"""
    response = client_create.post("/get_form", data={
        "date": '12.12.20', "phone": "7 98 89", 'email': 'gbdfail.ru'
    })

    assert response.status_code == 200
