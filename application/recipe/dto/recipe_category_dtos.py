from application.base.base_dto import BaseDto


class BaseRecipeCategoryDto(BaseDto):
    pass 


class RecipeCategoryCreateDto(BaseRecipeCategoryDto):
    name: str
    
    
class CategoryDto(RecipeCategoryCreateDto):
    id: int
    
    
class RecipeCategoryUpdateDto(BaseRecipeCategoryDto):
    name: str
