from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.ingredient_measurement_unit_dtos import IngredientMeasurementUnitCreateDto, IngredientMeasurementUnitDto, IngredientMeasurementUnitUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service


ingredient_measurement_unit_router = APIRouter()


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
