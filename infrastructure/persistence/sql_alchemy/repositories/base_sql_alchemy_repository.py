from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseSqlAlchemyRepository(ABC):

    @abstractmethod
    def __init__(self, session: Session):
        self._session = session
