import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from application.account_management.services.user_profile_service import UserProfileService
from application.authentication.services.user_service import UserService
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.User import UserOrmModel
from infrastructure.persistence.sql_alchemy.models.UserProfile import UserProfileOrmModel
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.user_profile_repository import UserProfileSqlAlchemyRepository
from presentation.dependencies import get_user_service, get_user_profile_service
from presentation.http.fastapi.main import app


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

    def override_get_user_profile_service():
        user_repository = UserSqlAlchemyRepository(session_)
        user_profile_repository = UserProfileSqlAlchemyRepository(session_)
        return UserProfileService(user_repository=user_repository, user_profile_respository=user_profile_repository)

    with TestClient(app) as client:
        app.dependency_overrides[get_user_service] = override_get_user_service
        app.dependency_overrides[get_user_profile_service] = override_get_user_profile_service
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(session_, engine):
    session_.add_all([
        UserOrmModel(username="username1", email="email1@email.com", password="password1"),
        UserProfileOrmModel(first_name='first_name', last_name='last_name', age=18, profile_picture='profilepicturelocation', user_id=1),
        UserProfileOrmModel(first_name='first_name2', last_name='last_name2', age=19, profile_picture='profilepicturelocation2', user_id=1)
    ])
    session_.commit()


def test_get_user_profile_200(seed_data, client):
    response = client.get("/users/1/user-profiles/1")
    expected_result = {
        "id": 1,
        "first_name": "first_name",
        "last_name": "last_name",
        "age": 18,
        "profile_picture": "profilepicturelocation",
        "user_id": 1
    }
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_get_user_profile_404(seed_data, client):
    response = client.get("/users/1/user-profiles/404")
    assert response.status_code == 404


def test_get_all_user_profiles_200(seed_data, client):
    response = client.get("/users/1/user-profiles/")
    expected_result = [
        {
            "id": 1,
            "first_name": "first_name",
            "last_name": "last_name",
            "age": 18,
            "profile_picture": "profilepicturelocation",
            "user_id": 1
        },
        {
            "id": 2,
            "first_name": "first_name2",
            "last_name": "last_name2",
            "age": 19,
            "profile_picture": "profilepicturelocation2",
            "user_id": 1
        },
    ]
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_get_all_user_profile_404(seed_data, client):
    response = client.get("/users/404/user-profiles")
    assert response.status_code == 404


def test_create_user_profile_201(seed_data, client: TestClient):
    payload = {
        "first_name": "first_name",
        "last_name": "last_name",
        "age": 18,
        "profile_picture": "profilepicturelocation",
        "user_id": 1
    }
    expected_result = {
        "id": 3,
        "first_name": "first_name",
        "last_name": "last_name",
        "age": 18,
        "profile_picture": "profilepicturelocation",
        "user_id": 1
    }
    response = client.post("/users/1/user-profiles/", json=payload)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response == expected_result


def test_create_user_profile_wrong_types_422(seed_data, client: TestClient):
    payload = {
        "first_name": 1,
        "last_name": 1,
        "age": "dezoito",
        "profile_picture": 1
    }
    response = client.post("/users/1/user-profiles/", json=payload)
    assert response.status_code == 422
    json_response = response.json()
    assert len(json_response["detail"]) == 4


def test_create_user_profile_missing_values_422(seed_data, client: TestClient):
    payload = {
    }
    response = client.post("/users/1/user-profiles/", json=payload)
    assert response.status_code == 422
    json_response = response.json()
    assert len(json_response["detail"]) == 4


def test_update_user_profile_200(seed_data, client: TestClient):
    payload = {
        "first_name": "updated_first_name",
        "last_name": "updated_last_name",
        "age": 19,
        "profile_picture": "updated_profilepicturelocation",
    }
    expected_result = {
        "id": 1,
        "first_name": "updated_first_name",
        "last_name": "updated_last_name",
        "age": 19,
        "profile_picture": "updated_profilepicturelocation",
        "user_id": 1
    }
    response = client.put("/users/1/user-profiles/1", json=payload)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == expected_result


def test_update_user_profile_wrong_types_422(seed_data, client: TestClient):
    payload = {
        "first_name": 1,
        "last_name": 1,
        "age": "dezoito",
        "profile_picture": 1
    }
    response = client.put("/users/1/user-profiles/1", json=payload)
    assert response.status_code == 422
    json_response = response.json()
    assert len(json_response["detail"]) == 4


def test_delete_user_profile_204(seed_data, client: TestClient):
    response = client.delete("/users/1/user-profiles/1")
    assert response.status_code == 204


def test_delete_user_profile_404(seed_data, client: TestClient):
    response = client.delete("/users/1/user-profiles/404")
    assert response.status_code == 404
