import os

import redis

from dotenv import load_dotenv

from application.authentication.services.authentication_service import AuthenticationService
from application.authentication.services.user_service import UserService
from application.account_management.services.user_profile_service import UserProfileService
from application.recipe.services.recipe_service import RecipeService
from infrastructure.cache.redis_cache_service import RedisCacheService
from infrastructure.persistence.sql_alchemy.database import SqlAlchemySession
from infrastructure.persistence.sql_alchemy.repositories.ingredient_repository import IngredientSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_category_repository import RecipeCategorySqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_ingredient_repository import RecipeIngredientSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.ingredient_measurement_unit_repository import IngredientMeasurementUnitSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.recipe_repository import RecipeSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.repositories.user_profile_repository import UserProfileSqlAlchemyRepository


load_dotenv()


def get_user_service():
    with SqlAlchemySession() as db:
        user_repository = UserSqlAlchemyRepository(db)
        yield UserService(user_repository)


def get_authentication_service():
    with SqlAlchemySession() as db:
        redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)
        cache_service = RedisCacheService(redis_client)
        user_repository = UserSqlAlchemyRepository(db)
        yield AuthenticationService(user_repository=user_repository, cache_service=cache_service)


def get_user_profile_service():
    with SqlAlchemySession() as db:
        user_repository = UserSqlAlchemyRepository(db)
        user_profile_repository = UserProfileSqlAlchemyRepository(db)
        yield UserProfileService(
            user_profile_respository=user_profile_repository,
            user_repository=user_repository
        )


def get_recipe_service():
    with SqlAlchemySession() as db:
        ingredient_repository = IngredientSqlAlchemyRepository(db)
        ingredient_measurement_unit_repository = IngredientMeasurementUnitSqlAlchemyRepository(db)
        recipe_ingredient_repository = RecipeIngredientSqlAlchemyRepository(db)
        recipe_repository = RecipeSqlAlchemyRepository(db)
        recipe_category_repository = RecipeCategorySqlAlchemyRepository(db)

        yield RecipeService(
            ingredient_repository=ingredient_repository,
            ingredient_measurement_unit_repository=ingredient_measurement_unit_repository,
            recipe_ingredient_repository=recipe_ingredient_repository,
            recipe_repository=recipe_repository,
            recipe_category_repository=recipe_category_repository
        )
