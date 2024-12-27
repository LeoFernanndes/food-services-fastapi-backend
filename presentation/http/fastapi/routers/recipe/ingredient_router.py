from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.ingredient import IngredientCreateDto, IngredientDto, IngredientUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service


ingredient_router = APIRouter()

@ingredient_router.post('/', status_code=201)
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
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')
