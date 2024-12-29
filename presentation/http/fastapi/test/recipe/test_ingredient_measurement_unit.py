import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from application.account_management.services.user_profile_service import UserProfileService
from application.authentication.services.user_service import UserService
from application.recipe.services.recipe_service import RecipeService
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Ingredient import IngredientOrmModel
from infrastructure.persistence.sql_alchemy.models.IngredientMeasurementUnit import IngredientMeasurementUnitOrmModel
from infrastructure.persistence.sql_alchemy.models.Recipes import RecipeOrmModel
from infrastructure.persistence.sql_alchemy.models.RecipeCategory import RecipeCategoryOrmModel
from infrastructure.persistence.sql_alchemy.models.RecipeIngredient import RecipeIngredientOrmModel
from infrastructure.persistence.sql_alchemy.models.User import UserOrmModel
from infrastructure.persistence.sql_alchemy.models.UserProfile import UserProfileOrmModel
from infrastructure.persistence.sql_alchemy.repositories.ingredient_measurement_unit_repository import \
    IngredientMeasurementUnitSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.ingredient_repository import IngredientSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_category_repository import \
    RecipeCategorySqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_ingredient_repository import \
    RecipeIngredientSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_repository import RecipeSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.user_profile_repository import UserProfileSqlAlchemyRepository
from presentation.dependencies import get_recipe_service, get_user_service, get_user_profile_service
from presentation.http.fastapi.main import app


# TODO: Delete ingredient measurement unit with foreign key contraint behaves as expected in the api but not in tests


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

    def override_get_recipe_service():
        ingredient_repository = IngredientSqlAlchemyRepository(session_)
        ingredient_measurement_unit_repository = IngredientMeasurementUnitSqlAlchemyRepository(session_)
        recipe_ingredient_repository = RecipeIngredientSqlAlchemyRepository(session_)
        recipe_repository = RecipeSqlAlchemyRepository(session_)
        recipe_category_repository = RecipeCategorySqlAlchemyRepository(session_)

        return RecipeService(
            ingredient_repository=ingredient_repository,
            ingredient_measurement_unit_repository=ingredient_measurement_unit_repository,
            recipe_ingredient_repository=recipe_ingredient_repository,
            recipe_repository=recipe_repository,
            recipe_category_repository=recipe_category_repository
        )

    with TestClient(app) as client:
        app.dependency_overrides[get_user_service] = override_get_user_service
        app.dependency_overrides[get_user_profile_service] = override_get_user_profile_service
        app.dependency_overrides[get_recipe_service] = override_get_recipe_service
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(session_, engine):
    session_.add_all([
        UserOrmModel(username="username1", email="email1@email.com", password="password1"),
        UserProfileOrmModel(first_name='first_name', last_name='last_name', age=18, profile_picture='profilepicturelocation', user_id=1),
        RecipeCategoryOrmModel(name='soup'),
        IngredientMeasurementUnitOrmModel(name='kg'),
        IngredientMeasurementUnitOrmModel(name='l'),
        IngredientMeasurementUnitOrmModel(name='cup'),
        IngredientOrmModel(name='feijão'),
        RecipeOrmModel(
            name='feijoada', title='feijoada', description='feijão temperado com carnes', user_profile_id=1,
            preparation_time_minutes=120, preparation_steps='steps', main_image='image_url', portions_quantity=10,
            category_id=1
        ),
        RecipeIngredientOrmModel(quantity=10, ingredient_id=1, ingredient_measurement_unit_id=1, recipe_id=1)
    ])
    session_.commit()


def test_get_ingredient_measurement_units_200(seed_data, client):
    response = client.get("/recipes-management/ingredient-measurement-units/")
    expected_result = [
        {
            "id": 1,
            "name": "kg"
        },
        {
            "id": 2,
            "name": "l"
        },
        {
            "id": 3,
            "name": "cup"
        }
    ]
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_get_ingredient_measurement_unit_200(seed_data, client):
    response = client.get("/recipes-management/ingredient-measurement-units/1")
    expected_result = {
            "id": 1,
            "name": "kg"
        }
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_get_ingredient_measurement_unit_404(seed_data, client):
    response = client.get("/recipes-management/ingredient-measurement-units/404")
    json_response = response.json()
    assert response.status_code == 404


def test_post_ingredient_measurement_unit_201(seed_data, client):
    payload = {
        'name': 'spoon'
    }
    response = client.post("/recipes-management/ingredient-measurement-units", json=payload)
    expected_result = {
            "id": 4,
            "name": "spoon"
        }
    json_response = response.json()
    assert response.status_code == 201
    assert json_response == expected_result
    

def test_post_ingredient_measurement_unit_missing_fields_422(seed_data, client):
    payload = {}
    response = client.post('/recipes-management/ingredient-measurement-units', json=payload)
    expected_result = {
        'detail': {
            'name': ['Field required']
        }
    }
    assert response.status_code == 422
    assert response.json() == expected_result


def test_post_ingredient_measurement_unit_400(seed_data, client):
    payload = {
        'name': 'kg'
    }
    response = client.post("/recipes-management/ingredient-measurement-units", json=payload)
    json_response = response.json()
    assert response.status_code == 400


def test_put_ingredient_measurement_unit_200(seed_data, client):
    payload = {
        'name': 'spoon'
    }
    response = client.put("/recipes-management/ingredient-measurement-units/1", json=payload)
    expected_result = {
            "id": 1,
            "name": "spoon"
        }
    json_response = response.json()
    assert response.status_code == 200
    assert json_response == expected_result


def test_put_ingredient_measurement_unit_missing_fields_422(seed_data, client):
    payload = {}
    response = client.put('/recipes-management/ingredient-measurement-units/1', json=payload)
    expected_result = {
        'detail': {
            'name': ['Field required']
        }
    }
    assert response.status_code == 422
    assert response.json() == expected_result


def test_put_ingredient_measurement_unit_404(seed_data, client):
    payload = {
        'name': 'l'
    }
    response = client.put("/recipes-management/ingredient-measurement-units/404", json=payload)
    assert response.status_code == 404


def test_put_ingredient_measurement_unit_400(seed_data, client):
    payload = {
        'name': 'l'
    }
    response = client.put("/recipes-management/ingredient-measurement-units/1", json=payload)
    assert response.status_code == 400


def test_delete_ingredient_measurement_unit_204(seed_data, client):
    response = client.delete("/recipes-management/ingredient-measurement-units/2")
    assert response.status_code == 204


# def test_delete_ingredient_measurement_unit_with_pk_constraint_400(seed_data, client):
#     response = client.delete("/recipes-management/ingredient-measurement-units/1")
#     assert response.status_code == 400


def test_delete_ingredient_measurement_unit_404(seed_data, client):
    response = client.delete("/recipes-management/ingredient-measurement-units/4")
    assert response.status_code == 404
