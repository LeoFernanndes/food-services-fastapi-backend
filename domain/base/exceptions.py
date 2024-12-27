class BaseDomainException(Exception):
    pass


class DatabaseIntegrityDomainException(BaseDomainException):
    pass


class NotFoundDomainException(BaseDomainException):
    pass
