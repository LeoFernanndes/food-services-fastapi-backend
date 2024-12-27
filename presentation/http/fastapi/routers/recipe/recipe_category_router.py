from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.base import exceptions as application_exceptions
from application.recipe.dto.recipe_category_dtos import RecipeCategoryCreateDto, CategoryDto, RecipeCategoryUpdateDto
from application.recipe.services.recipe_service import RecipeService
from presentation.dependencies import get_recipe_service


recipe_category_router = APIRouter()


@recipe_category_router.post('/', status_code=201)
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
