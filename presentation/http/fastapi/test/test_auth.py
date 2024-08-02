import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from application.authentication.services.authentication_service import AuthenticationService
from application.authentication.services.user_service import UserService
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository
from presentation.http.fastapi.main import app
from presentation.dependencies import get_authentication_service, get_user_service


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

    def override_get_authentication_service():
        user_repository = UserSqlAlchemyRepository(session_)
        return AuthenticationService(user_repository=user_repository)

    def override_get_user_service():
        user_repository = UserSqlAlchemyRepository(session_)
        return UserService(user_repository=user_repository)

    with TestClient(app) as client:
        app.dependency_overrides[get_authentication_service] = override_get_authentication_service
        app.dependency_overrides[get_user_service] = override_get_user_service
        yield client

    app.dependency_overrides.clear()


def create_user(client: TestClient):
    create_user_payload = {
        "username": "username",
        "email": "email@email.com",
        "password": "password"
    }
    expected_result = {
        "id": 1,
        "username": "username",
        "email": "email@email.com"
    }
    return client.post("/users", json=create_user_payload)


def test_login_for_access_token_200(client):
    response = create_user(client)
    assert response.status_code == 201
    response_auth = client.post("/auth/token/", data={"username": "username", "password": "password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    json_response_auth = response_auth.json()
    assert json_response_auth.get("token_type") == "bearer"


def test_login_for_access_token_with_unexistent_user_401(client):
    response = client.post("/auth/token/", data={"username": "username", "password": "password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    assert response.status_code == 401


def test_login_for_access_token_with_wrong_password_401(client):
    user_create_response = create_user(client)
    assert user_create_response.status_code == 201
    response = client.post("/auth/token/", data={"username": "username", "password": "wrong_password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    assert response.status_code == 401


def test_who_am_i_200(client):
    user_create_response = create_user(client)
    assert user_create_response.status_code == 201
    login_response = client.post("/auth/token/", data={"username": "username", "password": "password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    me_response = client.get("/auth/me/", headers=[("authorization", f"bearer {access_token}")])
    assert me_response.status_code == 200
    me_response_json = me_response.json()
    assert me_response_json["username"] == "username"


def test_refresh_auth_and_refresh_tokens_200(client):
    user_create_response = create_user(client)
    assert user_create_response.status_code == 201
    login_response = client.post("/auth/token/", data={"username": "username", "password": "password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]
    refresh_response = client.post("/auth/refresh/", headers=[("refresh", refresh_token)])
    assert refresh_response.status_code == 200

"""
TODO: check what makes tests related to cache fail intermittently

def test_refresh_auth_and_refresh_tokens_repeated_token_401(client):
    user_create_response = create_user(client)
    assert user_create_response.status_code == 201
    login_response = client.post("/auth/token/", data={"username": "username", "password": "password"}, headers=[("content-type", "application/x-www-form-urlencoded")])
    assert login_response.status_code == 200
    # tokens
    access_token = login_response.json()["access_token"]
    refresh_token = login_response.json()["refresh_token"]
    # first refresh 200
    refresh_response = client.post("/auth/refresh/", headers=[("refresh", refresh_token)])
    assert refresh_response.status_code == 200
    # get my info 200
    me_response = client.get("/auth/me/", headers=[("authorization", f"bearer {access_token}")])
    assert me_response.status_code == 200
    # refresh leaked token 401
    refresh_response = client.post("/auth/refresh/", headers=[("refresh", refresh_token)])
    assert refresh_response.status_code == 401
    # get my info revoked token 401
    me_response = client.get("/auth/me/", headers=[("authorization", f"bearer {access_token}")])
    assert me_response.status_code == 401
"""