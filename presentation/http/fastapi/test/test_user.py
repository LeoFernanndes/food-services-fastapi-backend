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
def seed_data(session_):
    session_.add_all([
        UserOrmModel(id=1, username="username1", email="email1@email.com", password="password1"),
        UserOrmModel(id=2, username="username2", email="email2@email.com", password="password2"),
        UserOrmModel(id=3, username="username3", email="email3@email.com", password="password3"),
        UserOrmModel(id=4, username="username4", email="email4@email.com", password="password4"),
        UserOrmModel(id=5, username="username5", email="email5@email.com", password="password5"),
    ])
    session_.commit()


def test_get_user_200(seed_data, client):
    response = client.get("/users/1")
    json_response = response.json()
    assert json_response["id"] == 1
