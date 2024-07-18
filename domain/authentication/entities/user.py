from domain.base.base_entity import BaseEntity


class User(BaseEntity):
    def __init__(self, id: int | None, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
