from typing import Self

from domain.base.base_entity import BaseEntity


class RecipeCategory(BaseEntity):
    def __init__(self, id: int | None, name: str) -> Self:
        self.id = id
        self.name = name
