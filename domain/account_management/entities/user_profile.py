from domain.base.base_entity import BaseEntity


class UserProfile(BaseEntity):
    def __init__(self, id: int | None, first_name: str, last_name: str, age: int, profile_picture: str, user_id: int):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.profile_picture = profile_picture
        self.user_id = user_id
