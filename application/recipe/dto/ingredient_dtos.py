from application.base.base_dto import BaseDto


class BaseIngredientDto(BaseDto):
    pass 


class IngredientCreateDto(BaseIngredientDto):
    name: str
    measurement_unit_id: int
    

class IngredientDto(IngredientCreateDto):
    id: int
    

class IngredientUpdateDto(BaseIngredientDto):
    name: str
    measurement_unit_id: int
