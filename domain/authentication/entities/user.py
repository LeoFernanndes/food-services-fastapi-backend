from domain.base.base_entity import BaseEntity


class User(BaseEntity):
    def __init__(self, id: int | None, username: str, email: str, password: str):
        self.id = id  # pk, auto-increment
        self.username = username  # unique, not-null
        self.email = email  # unique, not-null
        self.password = password  # not-null
