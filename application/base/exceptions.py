class BaseApplicationException(Exception):
    pass


class EntityNotFoundApplicationException(BaseApplicationException):
    pass


class EntityValidationApplicationException(BaseApplicationException):
    pass
