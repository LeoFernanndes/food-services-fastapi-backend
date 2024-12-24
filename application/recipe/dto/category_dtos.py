from application.base.base_dto import BaseDto


class BaseCategoryDto(BaseDto):
    pass 


class CategoryCreateDto(BaseCategoryDto):
    name: str
    
    
class CategoryDto(CategoryCreateDto):
    id: int
    
    
class CategoryUpdateDto(BaseCategoryDto):
    name: str
