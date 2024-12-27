from fastapi import APIRouter

from presentation.http.fastapi.routers.recipe.ingredient_measurement_unit_router import ingredient_measurement_unit_router
from presentation.http.fastapi.routers.recipe.ingredient_router import ingredient_router
from presentation.http.fastapi.routers.recipe.recipe_category_router import recipe_category_router
from presentation.http.fastapi.routers.recipe.recipe_router import recipe_router


recipes_management_router = APIRouter()


recipes_management_router.include_router(ingredient_router, prefix='/ingredients')
recipes_management_router.include_router(ingredient_measurement_unit_router, prefix='/ingredient-measurement-units')
recipes_management_router.include_router(recipe_category_router, prefix='/recipe-categories')
recipes_management_router.include_router(recipe_router, prefix='/recipes')
