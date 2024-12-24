from application.base.base_dto import BaseDto


class BaseIngredientMeasurementUnitDto(BaseDto):
    pass

class IngredientMeasurementUnitCreateDto(BaseIngredientMeasurementUnitDto):
    name: str
    
class IngredientMeasurementUnitDto(IngredientMeasurementUnitCreateDto):
    id: int
    
class IngredientMeasurementUnitUpdateDto(BaseIngredientMeasurementUnitDto):
    name: str
