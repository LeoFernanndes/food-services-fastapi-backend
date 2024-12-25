from typing import List

from application.base import exceptions as application_exceptions
from application.recipe.dto.recipe_category_dtos import RecipeCategoryCreateDto, CategoryDto, RecipeCategoryUpdateDto
from application.recipe.dto.ingredient_dtos import IngredientCreateDto, IngredientDto, IngredientUpdateDto
from application.recipe.dto.ingredient_measurement_unit_dtos import IngredientMeasurementUnitCreateDto, IngredientMeasurementUnitDto, IngredientMeasurementUnitUpdateDto
from application.recipe.dto.recipe_dtos import RecipeCreateDto, RecipeDto, RecipeUpdateDto
from domain.account_management.repositories.user_profile_repository import UserProfileRepository
from domain.base import exceptions as domain_exceptions
from domain.recipes.entities.recipe_category import RecipeCategory
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit
from domain.recipes.repositories.recipe_category_repository import RecipeCategoryRepository
from domain.recipes.repositories.ingredient_measurement_unit_repository import IngredientMeasurementUnitRepository
from domain.recipes.repositories.ingredient_repository import IngredientRepository
from domain.recipes.repositories.recipe_repository import RecipeRepository


class RecipeService:
    def __init__(
        self,
        ingredient_category_repository: RecipeCategoryRepository,
        ingredient_measurement_unit_repository: IngredientMeasurementUnitRepository,
        # ingredient_repository: IngredientRepository,
        # recipe_repository: RecipeRepository,
        # user_profile_repository: UserProfileRepository
    ):
        self._category_repository = ingredient_category_repository
        self._ingredient_measurement_unit_repository = ingredient_measurement_unit_repository
        # self.ingredient_repository = ingredient_repository
        # self.recipe_repository = recipe_repository
        # self.user_profile_repository = user_profile_repository
        
    def create_ingredient_measurement_unit(self, crate_dto: IngredientMeasurementUnitCreateDto) -> IngredientMeasurementUnitDto:
        payload_entity = IngredientMeasurementUnit(id=None, name=crate_dto.name)
        try:
            created_entity = self._ingredient_measurement_unit_repository.save(payload_entity)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return IngredientMeasurementUnitDto(id=created_entity.id, name=created_entity.name)

    def list_ingredient_measurement_units(self, limit: int = 1000, offset: int = 0) -> List[IngredientMeasurementUnitDto]:
        entities = self._ingredient_measurement_unit_repository.get_all(limit, offset)
        return [IngredientMeasurementUnitDto(id=e.id, name=e.name) for e in entities]

    def get_ingredient_measurement_unit(self, id: int) -> IngredientMeasurementUnitDto:
        try:
            entity = self._ingredient_measurement_unit_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return IngredientMeasurementUnitDto(id=entity.id, name=entity.name)

    def update_ingredient_measurement_unit(self, id: int, update_dto: IngredientMeasurementUnitUpdateDto) -> IngredientMeasurementUnitDto:
        try:
            entity = self._ingredient_measurement_unit_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        entity.name = update_dto.name
        try:
            updated_dto = self._ingredient_measurement_unit_repository.save(entity)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return IngredientMeasurementUnitDto(id=updated_dto.id, name=updated_dto.name)

    def delete_ingredient_measurement_unit(self, id: int) -> None:
        try:
            entity = self._ingredient_measurement_unit_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        self._ingredient_measurement_unit_repository.delete(id)
        return None

    def create_recipe_category(self, category_create_dto: RecipeCategoryCreateDto) -> CategoryDto:
        category_entity = RecipeCategory(id=None, name=category_create_dto.name)
        try:
            created_category = self._category_repository.save(category_entity)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return CategoryDto(id=created_category.id, name=created_category.name)

    def list_recipe_categories(self, limit: int = 1000, offset: int = 0) -> List[CategoryDto]:
        return [CategoryDto(id=c.id, name=c.name) for c in self._category_repository.get_all(limit=limit, offset=offset)]

    def get_recipe_category(self, id: int) -> CategoryDto:
        try:
            category_entity = self._category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return CategoryDto(id=category_entity.id, name=category_entity.name)

    def update_recipe_category(self, id: int, category_update_dto: RecipeCategoryUpdateDto) -> CategoryDto:
        try:
            category_entity = self._category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        category_entity.name = category_update_dto.name
        updated_entity = self._category_repository.save(category_entity)
        return CategoryDto(id=updated_entity.id, name=updated_entity.name)

    def delete_recipe_category(self, id) -> None:
        try:
            self._category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return self._category_repository.delete(id)
