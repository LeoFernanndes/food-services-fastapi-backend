from application.base.base_dto import BaseDto


class BaseRecipeIngredientDto(BaseDto):
    pass 


class RecipeIngredientCreateDto(BaseRecipeIngredientDto):
    quantity: int
    ingredient_id: int
    measurement_unit_id: int


class RecipeIngredientDto(RecipeIngredientCreateDto):
    id: int
    recipe_id: int
    

class RecipeIngredientUpdateDto(BaseRecipeIngredientDto):
    quantity: int
    measurement_unit_id: int
