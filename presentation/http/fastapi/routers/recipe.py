from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.ingredient import IngredientCreateDto, IngredientDto, IngredientUpdateDto
from application.recipe.dto.recipe_ingredient_dtos import RecipeIngredientCreateDto, RecipeIngredientDto, RecipeIngredientUpdateDto
from application.recipe.dto.ingredient_measurement_unit_dtos import IngredientMeasurementUnitCreateDto, IngredientMeasurementUnitDto, IngredientMeasurementUnitUpdateDto
from application.recipe.dto.recipe_category_dtos import RecipeCategoryCreateDto, CategoryDto, RecipeCategoryUpdateDto
from application.recipe.dto.recipe_dtos import RecipeCreateDto, RecipeDto, RecipeUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service


# TODO: remove 200 from successful delete response status on swagger

recipes_management_router = APIRouter()

ingredient_router = APIRouter()
ingredient_measurement_unit_router = APIRouter()
recipe_ingredient_router = APIRouter()
recipe_router = APIRouter()
recipe_category_router = APIRouter()


@ingredient_measurement_unit_router.post('/')
def create_ingredient_measurement_unit(create_dto: IngredientMeasurementUnitCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientMeasurementUnitDto:
    try:
        return recipe_service.create_ingredient_measurement_unit(create_dto)
    except application_exceptions.EntityValidationApplicationException as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@ingredient_measurement_unit_router.get('/')
def list_ingredient_measurement_units(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[IngredientMeasurementUnitDto]:
    try:
        return recipe_service.list_ingredient_measurement_units(limit=items_per_page, offset=page)
    except Exception as e:
        raise HTTPException(status_code=500)


@ingredient_measurement_unit_router.get('/{id}')
def get_ingredient_measurement_unit(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientMeasurementUnitDto:
    try:
        return recipe_service.get_ingredient_measurement_unit(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found.')
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_measurement_unit_router.put('/{id}')
def update_ingredient_measurement_unit(id: int, unit_update_dto: IngredientMeasurementUnitUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientMeasurementUnitDto:
    try:
        return recipe_service.update_ingredient_measurement_unit(id, unit_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found.')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400)
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_measurement_unit_router.delete('/{id}', status_code=204)
def delete_ingredient_measurement_unit(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_ingredient_measurement_unit(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found.')
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@recipe_category_router.post('/')
def create_recipe_category(category_create_dto: RecipeCategoryCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.create_recipe_category(category_create_dto)
    except application_exceptions.EntityValidationApplicationException as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@recipe_category_router.get('/')
def list_recipe_categories(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[CategoryDto]:
    try:
        return recipe_service.list_recipe_categories(limit=items_per_page, offset=page)
    except:
        raise HTTPException(500, detail='Internal server error.')


@recipe_category_router.get('/{id}')
def get_recipe_category(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.get_recipe_category(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found.')
    except:
        raise HTTPException(500, detail='Internal server error.')


@recipe_category_router.put('/{id}')
def update_recipe_category(id: int, category_update_dto: RecipeCategoryUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.update_recipe_category(id, category_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found.')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error.')


@recipe_category_router.delete('/{id}', status_code=204)
def delete_recipe_category(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_recipe_category(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')


@recipe_ingredient_router.post('/')
def create_recipe_ingredient(ingredient_create_dto: RecipeIngredientCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.create_recipe_ingredient(ingredient_create_dto)
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.get('/{id}')
def get_recipe_ingredient(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.get_recipe_ingredient(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.get('/')
def list_recipe_ingredients(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[RecipeIngredientDto]:
    try:
        return recipe_service.list_recipe_ingredients(limit=items_per_page, offset=page)
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.put('/{id}')
def update_recipe_ingredient(id: int, ingredient_update_dto: RecipeIngredientUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.update_recipe_ingredient(id, ingredient_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.delete('/{id}')
def delete_recipe_ingredient(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_recipe(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_router.post('/')
def create_recipe(recipe_create_dto: RecipeCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeDto:
    try:
        return recipe_service.create_recipe(recipe_create_dto)
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400,  detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_router.get('/{id}')
def get_recipe(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeDto:
    try:
        return recipe_service.get_recipe(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_router.get('/')
def list_recipes(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[RecipeDto]:
    try:
        return recipe_service.list_recipes(limit=items_per_page, offset=page)
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_router.put('/{id}')
def update_recipe(id: int, recipe_update_dto: RecipeUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeDto:
    try:
        return recipe_service.update_recipe(id, recipe_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server erro')


@recipe_router.delete('/{id}', status_code=204)
def delete_recipe(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_recipe(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@ingredient_router.post('/')
def create_ingredient(ingredient_create_dto: IngredientCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientDto:
    try:
        return recipe_service.create_ingredient(ingredient_create_dto)
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@ingredient_router.get('/{id}')
def get_ingredient(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientDto:
    try:
        return recipe_service.get_ingredient(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@ingredient_router.get('/')
def list_ingredients(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[IngredientDto]:
    try:
        return recipe_service.list_ingredients(limit=items_per_page, offset=page)
    except:
        HTTPException(500, detail='Internal server error')


@ingredient_router.put('/{id}')
def update_ingredient(id: int, ingredient_update_dto: IngredientUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientDto:
    try:
        return recipe_service.update_ingredient(id, ingredient_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        HTTPException(500, detail='Internal server error')


@ingredient_router.delete('/{id}', status_code=204)
def delete_ingredient(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_ingredient(id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


recipes_management_router.include_router(ingredient_router, prefix='/ingredient')
recipes_management_router.include_router(ingredient_measurement_unit_router, prefix='/ingredient-measurement-units')
recipes_management_router.include_router(recipe_ingredient_router, prefix='/recipe-ingredients')
recipes_management_router.include_router(recipe_router, prefix='/recipes')
recipes_management_router.include_router(recipe_category_router, prefix='/recipe-categories')
