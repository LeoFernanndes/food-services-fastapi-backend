from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.recipe_dtos import RecipeCreateDto, RecipeDto, RecipeUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service
from presentation.http.fastapi.routers.recipe.recipe_ingredient_router import recipe_ingredient_router

recipe_router = APIRouter()


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


recipe_router.include_router(recipe_ingredient_router, prefix='/{recipe_id}/recipe-ingredients')