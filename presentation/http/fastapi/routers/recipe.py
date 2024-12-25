from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base.exceptions import NotFoundEntity
from application.recipe.dto.category_dtos import CategoryCreateDto, CategoryDto, CategoryUpdateDto
from application.recipe.dto.ingredient_measurement_unit_dtos import IngredientMeasurementUnitCreateDto, IngredientMeasurementUnitDto, IngredientMeasurementUnitUpdateDto
from application.recipe.services.recipe_service import RecipeService
from domain.base.exceptions import DatabaseIntegrityError, NotFoundDomainException
from presentation.dependencies import get_recipe_service


# TODO: remove 200 from successful delete response status on swagger

recipes_management_router = APIRouter()

ingredient_measurement_unit_router = APIRouter()
ingredient_category_router = APIRouter()


@ingredient_measurement_unit_router.post('/')
def create_ingredient_measurement_unit(create_dto: IngredientMeasurementUnitCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientMeasurementUnitDto:
    try:
        return recipe_service.create_ingredient_measurement_unit(create_dto)
    except DatabaseIntegrityError as e:
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
    except NotFoundEntity:
        raise HTTPException(404, detail='Not found.')
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_measurement_unit_router.put('/{id')
def update_ingredient_measurement_unit(id: int, unit_update_dto: IngredientMeasurementUnitUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> IngredientMeasurementUnitDto:
    try:
        return recipe_service.update_ingredient_measurement_unit(id, unit_update_dto)
    except NotFoundEntity:
        raise HTTPException(404, detail='Not found.')
    except DatabaseIntegrityError:
        raise HTTPException(400)
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_measurement_unit_router.delete('/{id}', status_code=204)
def delete_ingredient_measurement_unit(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_ingredient_measurement_unit(id)
    except NotFoundEntity:
        raise HTTPException(404, detail='Not found.')
    except Exception as e:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_category_router.post('/')
def create_ingredient_category(category_create_dto: CategoryCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.create_ingredient_category(category_create_dto)
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@ingredient_category_router.get('/')
def list_ingredient_categories(recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[CategoryDto]:
    return recipe_service.list_ingredient_categories(limit=items_per_page, offset=page)


@ingredient_category_router.get('/{id}')
def get_ingredient_category(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.get_ingredient_category(id)
    except NotFoundDomainException:
        raise HTTPException(404, detail='Not found.')
    except:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_category_router.put('/{id}')
def update_ingredient_category(id: int, category_update_dto: CategoryUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> CategoryDto:
    try:
        return recipe_service.update_ingredient_category(id, category_update_dto)
    except NotFoundEntity:
        raise HTTPException(404, detail='Not found.')
    except DatabaseIntegrityError:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error.')


@ingredient_category_router.delete('/{id}', status_code=204)
def delete_ingredient_category(id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_ingredient_category(id)
    except NotFoundEntity:
        raise HTTPException(404, detail='Not found')


recipes_management_router.include_router(ingredient_measurement_unit_router, prefix='/ingredient-measurement-units')
recipes_management_router.include_router(ingredient_category_router, prefix='/ingredient-categories')
