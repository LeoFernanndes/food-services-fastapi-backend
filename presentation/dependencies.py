from application.authentication.services.authentication_service import AuthenticationService
from application.authentication.services.user_service import UserService
from infrastructure.persistence.sql_alchemy.database import SqlAlchemySession
from infrastructure.persistence.sql_alchemy.repositories.user_repository import UserSqlAlchemyRepository


def get_user_service():
    with SqlAlchemySession() as db:
        user_repository = UserSqlAlchemyRepository(db)
        yield UserService(user_repository)


def get_authentication_service():
    with SqlAlchemySession() as db:
        user_repository = UserSqlAlchemyRepository(db)
        yield AuthenticationService(user_repository)
