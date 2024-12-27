from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.recipe_ingredient_dtos import RecipeIngredientCreateDto, RecipeIngredientDto, RecipeIngredientUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service


# TODO: Check if there is a better wat to seggregate nested routers declaring parenti resource ids

recipe_ingredient_router = APIRouter()


@recipe_ingredient_router.post('/')
def create_recipe_ingredient(recipe_id: int, ingredient_create_dto: RecipeIngredientCreateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.create_recipe_ingredient(recipe_id=recipe_id, recipe_ingredient_create_dto=ingredient_create_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.get('/{id}')
def get_recipe_ingredient(recipe_id: int, id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.get_recipe_ingredient(recipe_id=recipe_id, id=id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.get('/')
def list_recipe_ingredients(recipe_id: int, recipe_service: RecipeService = Depends(get_recipe_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[RecipeIngredientDto]:
    try:
        return recipe_service.list_recipe_ingredients(recipe_id=recipe_id, limit=items_per_page, offset=page)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.put('/{id}')
def update_recipe_ingredient(recipe_id: int, id: int, ingredient_update_dto: RecipeIngredientUpdateDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeIngredientDto:
    try:
        return recipe_service.update_recipe_ingredient(recipe_id=recipe_id, id=id, ingredient_update_dto=ingredient_update_dto)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except application_exceptions.EntityValidationApplicationException:
        raise HTTPException(400, detail='Bad request')
    except:
        raise HTTPException(500, detail='Internal server error')


@recipe_ingredient_router.delete('/{id}')
def delete_recipe_ingredient(recipe_id: int, id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> None:
    try:
        return recipe_service.delete_recipe_ingredient(recipe_id=recipe_id, id=id)
    except application_exceptions.EntityNotFoundApplicationException:
        raise HTTPException(404, detail='Not found')
    except:
        raise HTTPException(500, detail='Internal server error')
