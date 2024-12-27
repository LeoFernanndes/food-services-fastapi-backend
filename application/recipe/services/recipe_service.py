from typing import List

from application.base import exceptions as application_exceptions
from application.recipe.dto.ingredient import IngredientCreateDto, IngredientDto, IngredientUpdateDto
from application.recipe.dto.recipe_category_dtos import RecipeCategoryCreateDto, CategoryDto, RecipeCategoryUpdateDto
from application.recipe.dto.recipe_ingredient_dtos import RecipeIngredientCreateDto, RecipeIngredientDto, RecipeIngredientUpdateDto
from application.recipe.dto.ingredient_measurement_unit_dtos import IngredientMeasurementUnitCreateDto, IngredientMeasurementUnitDto, IngredientMeasurementUnitUpdateDto
from application.recipe.dto.recipe_dtos import RecipeCreateDto, RecipeDto, RecipeUpdateDto
from domain.account_management.repositories.user_profile_repository import UserProfileRepository
from domain.base import exceptions as domain_exceptions
from domain.recipes.entities.ingredient import Ingredient
from domain.recipes.entities.recipe_ingredient import RecipeIngredient
from domain.recipes.entities.recipe import Recipe
from domain.recipes.entities.recipe_category import RecipeCategory
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit
from domain.recipes.repositories.ingredient_repository import IngredientRepository
from domain.recipes.repositories.recipe_category_repository import RecipeCategoryRepository
from domain.recipes.repositories.ingredient_measurement_unit_repository import IngredientMeasurementUnitRepository
from domain.recipes.repositories.recipe_ingredient_repository import RecipeIngredientRepository
from domain.recipes.repositories.recipe_repository import RecipeRepository


class RecipeService:
    def __init__(
        self,
        ingredient_repository: IngredientRepository,
        ingredient_measurement_unit_repository: IngredientMeasurementUnitRepository,
        recipe_ingredient_repository: RecipeIngredientRepository,
        recipe_category_repository: RecipeCategoryRepository,
        recipe_repository: RecipeRepository,
        # user_profile_repository: UserProfileRepository
    ):
        self._ingredient_repository = ingredient_repository
        self._ingredient_measurement_unit_repository = ingredient_measurement_unit_repository
        self._recipe_ingredient_repository = recipe_ingredient_repository
        self._recipe_category_repository = recipe_category_repository
        self._recipe_repository = recipe_repository
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
            created_category = self._recipe_category_repository.save(category_entity)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return CategoryDto(id=created_category.id, name=created_category.name)

    def list_recipe_categories(self, limit: int = 1000, offset: int = 0) -> List[CategoryDto]:
        return [CategoryDto(id=c.id, name=c.name) for c in self._recipe_category_repository.get_all(limit=limit, offset=offset)]

    def get_recipe_category(self, id: int) -> CategoryDto:
        try:
            category_entity = self._recipe_category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return CategoryDto(id=category_entity.id, name=category_entity.name)

    def update_recipe_category(self, id: int, category_update_dto: RecipeCategoryUpdateDto) -> CategoryDto:
        try:
            category_entity = self._recipe_category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        category_entity.name = category_update_dto.name
        updated_entity = self._recipe_category_repository.save(category_entity)
        return CategoryDto(id=updated_entity.id, name=updated_entity.name)

    def delete_recipe_category(self, id) -> None:
        try:
            self._recipe_category_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return self._recipe_category_repository.delete(id)

    def create_recipe_ingredient(self, recipe_ingredient_create_dto: RecipeIngredientCreateDto) -> RecipeIngredientDto:
        ingredient = RecipeIngredient(id=None, quantity=recipe_ingredient_create_dto.quantity, ingredient_id=recipe_ingredient_create_dto.ingredient_id, ingredient_measurement_unit_id=recipe_ingredient_create_dto.measurement_unit_id, recipe_id=recipe_ingredient_create_dto.recipe_id)
        try:
            created_ingredient = self._recipe_ingredient_repository.save(ingredient)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return RecipeIngredientDto(id=created_ingredient.id, quantity=created_ingredient.quantity, ingredient_id=created_ingredient.ingredient_id, measurement_unit_id=created_ingredient.ingredient_measurement_unit_id, recipe_id=created_ingredient.recipe_id)

    def get_recipe_ingredient(self, id) -> RecipeIngredientDto:
        try:
            ingredient = self._recipe_ingredient_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException
        return RecipeIngredientDto(id=ingredient.id, quantity=ingredient.quantity, ingredient_id=ingredient.ingredient_id, measurement_unit_id=ingredient.ingredient_measurement_unit_id, recipe_id=ingredient.recipe_id)

    def list_recipe_ingredients(self, limit: int = 1000, offset: int = 0) -> List[RecipeIngredientDto]:
        ingredients = self._recipe_ingredient_repository.get_all(limit=limit, offset=offset)
        return [RecipeIngredientDto(id=i.id, quantity=i.quantity, ingredient_id=i.ingredient_id, recipe_id=i.recipe_id, measurement_unit_id=i.ingredient_measurement_unit_id) for i in ingredients]

    def update_recipe_ingredient(self, id: int, ingredient_update_dto: RecipeIngredientUpdateDto) -> RecipeIngredientDto:
        try:
            ingredient = self._recipe_ingredient_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        ingredient.ingredient_measurement_unit_id = ingredient_update_dto.measurement_unit_id
        ingredient.quantity = ingredient_update_dto.quantity
        try:
            updated_ingredient = self._recipe_ingredient_repository.save(ingredient)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()
        return RecipeIngredientDto(id=updated_ingredient.id, quantity=updated_ingredient.quantity, ingredient_id=updated_ingredient.ingredient_id, recipe_id=updated_ingredient.recipe_id, measurement_unit_id=updated_ingredient.ingredient_measurement_unit_id)

    def delete_recipe_ingredient(self, id) -> None:
        try:
            return self._recipe_ingredient_repository.delete(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()

    def create_recipe(self, recipe_create_dto: RecipeCreateDto) -> RecipeDto:
        recipe = Recipe(
            id=None, name=recipe_create_dto.name, title=recipe_create_dto.title, description=recipe_create_dto.description,
            user_profile_id=recipe_create_dto.user_profile_id, preparation_steps=recipe_create_dto.preparation_steps,
            preparation_time_minutes=recipe_create_dto.preparation_time_minutes, main_image=recipe_create_dto.main_image,
            portions_quantity=recipe_create_dto.portions_quantity, category_id=recipe_create_dto.category_id
        )
        try:
            created_recipe = self._recipe_repository.save(recipe)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException
        return RecipeDto(
            id=created_recipe.id, name=created_recipe.name, title=created_recipe.title, description=created_recipe.description,
            user_profile_id=created_recipe.user_profile_id, preparation_steps=created_recipe.preparation_steps,
            preparation_time_minutes=created_recipe.preparation_time_minutes, main_image=created_recipe.main_image,
            portions_quantity=created_recipe.portions_quantity, category_id=created_recipe.category_id
        )

    def get_recipe(self, id: int) -> RecipeDto:
        try:
            recipe = self._recipe_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException
        return RecipeDto(
            id=recipe.id, name=recipe.name, title=recipe.title, description=recipe.description,
            user_profile_id=recipe.user_profile_id, preparation_steps=recipe.preparation_steps,
            preparation_time_minutes=recipe.preparation_time_minutes, main_image=recipe.main_image,
            portions_quantity=recipe.portions_quantity, category_id=recipe.category_id
        )

    def list_recipes(self, limit: int = 1000, offset: int = 0) -> List[RecipeDto]:
        recipes = self._recipe_repository.get_all(limit=limit, offset=offset)
        recipe_dtos = []
        for recipe in recipes:
            recipe_dto = RecipeDto(
                id=recipe.id, name=recipe.name, title=recipe.title, description=recipe.description,
                user_profile_id=recipe.user_profile_id, preparation_steps=recipe.preparation_steps,
                preparation_time_minutes=recipe.preparation_time_minutes, main_image=recipe.main_image,
                portions_quantity=recipe.portions_quantity, category_id=recipe.category_id
            )
            recipe_dtos.append(recipe_dto)
        return recipe_dtos

    def update_recipe(self, id: int, recipe_update_dto: RecipeUpdateDto) -> RecipeDto:
        try:
            recipe = self._recipe_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()

        recipe.name = recipe_update_dto.name
        recipe.portions_quantity = recipe_update_dto.portions_quantity
        recipe.title = recipe_update_dto.title
        recipe.title = recipe_update_dto.title
        recipe.description = recipe_update_dto.description
        recipe.preparation_steps = recipe_update_dto.preparation_steps
        recipe.preparation_time_minutes = recipe_update_dto.preparation_time_minutes
        recipe.main_image = recipe_update_dto.main_image
        recipe.category_id = recipe_update_dto.category_id

        try:
            updated_recipe = self._recipe_repository.save(recipe)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException()

        return RecipeDto(
                id=updated_recipe.id, name=updated_recipe.name, title=updated_recipe.title, description=updated_recipe.description,
                user_profile_id=updated_recipe.user_profile_id, preparation_steps=updated_recipe.preparation_steps,
                preparation_time_minutes=updated_recipe.preparation_time_minutes, main_image=updated_recipe.main_image,
                portions_quantity=updated_recipe.portions_quantity, category_id=updated_recipe.category_id
            )

    def delete_recipe(self, id: int) -> None:
        try:
            recipe = self._recipe_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        return self._recipe_repository.delete(id)

    def create_ingredient(self, ingredient_create_dto: IngredientCreateDto) -> IngredientDto:
        try:
            ingredient = Ingredient(id=None, name=ingredient_create_dto.name)
            created_ingredient = self._ingredient_repository.save(ingredient)
            return IngredientDto(id=created_ingredient.id, name=created_ingredient.name)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException

    def list_ingredients(self, limit: int = 1000, offset: int = 0) -> List[IngredientDto]:
        ingredients = self._ingredient_repository.get_all(limit=limit, offset=offset)
        return [IngredientDto(id=i.id, name=i.name) for i in ingredients]

    def get_ingredient(self, id: int) -> IngredientDto:
        try:
            ingredient = self._ingredient_repository.get_by_id(id)
            return IngredientDto(id=ingredient.id, name=ingredient.name)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()

    def update_ingredient(self, id: int, ingredient_update_dto: IngredientUpdateDto) -> IngredientDto:
        try:
            ingredient = self._ingredient_repository.get_by_id(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
        ingredient.name = ingredient_update_dto.name
        try:
            updated_ingredient = self._ingredient_repository.save(ingredient)
        except domain_exceptions.DatabaseIntegrityDomainException:
            raise application_exceptions.EntityValidationApplicationException
        return IngredientDto(id=updated_ingredient.id, name=updated_ingredient.name)

    def delete_ingredient(self, id: int) -> None:
        try:
            return self._ingredient_repository.delete(id)
        except domain_exceptions.NotFoundDomainException:
            raise application_exceptions.EntityNotFoundApplicationException()
