from ninja.schema import Schema


class GetUserSchema(Schema):
    id: int
    username: str
    password: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    groups: list


class UserSchema(Schema):
    username: str
    password: str
    is_superuser: bool
    is_staff: bool
    is_active: bool


class Error(Schema):
    error: str


class Filters(Schema):
    limit: int = 100
    offset: int = None
    query: str = None


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    access_token: str
    refresh_token: str
