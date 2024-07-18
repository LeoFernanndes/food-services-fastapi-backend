from abc import ABC, abstractmethod

from domain.base.base_entity import BaseEntity


class BaseOrmModel:

    @abstractmethod
    def to_domain(self) -> BaseEntity:
        pass

    @staticmethod
    @abstractmethod
    def from_entity(entity: BaseEntity):
        pass
