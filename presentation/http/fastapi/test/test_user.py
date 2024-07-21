import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from application.authentication.services.user_service import UserService
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.User import UserOrmModel
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository
from presentation.http.fastapi.main import app
from presentation.http.fastapi.routers.user import get_user_service


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg2') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture
def session_(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as _session:
        yield _session
        _session.rollback()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session_):

    def override_get_user_service():
        user_repository = UserSqlAlchemyRepository(session_)
        return UserService(user_repository=user_repository)

    with TestClient(app) as client:
        app.dependency_overrides[get_user_service] = override_get_user_service
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(session_, engine):
    session_.add_all([
        UserOrmModel(username="username1", email="email1@email.com", password="password1"),
        UserOrmModel(username="username2", email="email2@email.com", password="password2"),
        UserOrmModel(username="username3", email="email3@email.com", password="password3"),
        UserOrmModel(username="username4", email="email4@email.com", password="password4"),
        UserOrmModel(username="username5", email="email5@email.com", password="password5")
    ])
    session_.commit()


def test_get_user_200(seed_data, client):
    response = client.get("/users/1")
    expected_result = {
        "id": 1,
        "username": "username1",
        "email": "email1@email.com"
    }
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_get_user_404(seed_data, client):
    response = client.get("/users/404")
    assert response.status_code == 404


def test_list_users_200(seed_data, client):
    response = client.get("/users")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 5


def test_create_user_201(seed_data, client: TestClient):
    payload = {
        "username": "username6",
        "email": "email6@email.com",
        "password": "password6"
    }
    expected_result = {
        "id": 6,
        "username": "username6",
        "email": "email6@email.com"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response == expected_result


def test_create_user_400(seed_data, client):
    payload = {
        "username": "username1",
        "email": "email1@email.com",
        "password": "password1"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response == {"detail": ["Duplicated username and or email."]}


def test_update_user_200(seed_data, client):
    payload = {
        "username": "updated_username6",
        "email": "updated_email6@email.com",
        "password": "updated_password6"
    }
    expected_result = {
        "id": 1,
        "username": "updated_username6",
        "email": "email1@email.com"
    }
    response = client.put("/users/1", json=payload)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == expected_result


def test_update_user_400(seed_data, client):
    payload = {
        "username": "username1",
        "email": "email1@email.com",
        "password": "password1"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response == {"detail": ["Duplicated username and or email."]}


def test_update_user_404(seed_data, client):
    payload = {
        "username": "username1",
        "email": "email1@email.com",
        "password": "password1"
    }
    response = client.put("/users/404", json=payload)
    assert response.status_code == 404


def test_delete_user(seed_data, client):
    response = client.delete("/users/1")
    assert response.status_code == 204
