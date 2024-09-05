from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from ninja import Query
from ninja import Router
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate
from rest_framework_simplejwt.tokens import RefreshToken

from test_django_ninja.users.models import User
from test_django_ninja.users.schemas import Filters
from test_django_ninja.users.schemas import GetUserSchema
from test_django_ninja.users.schemas import LoginSchema
from test_django_ninja.users.schemas import TokenSchema
from test_django_ninja.users.schemas import UserSchema
from test_django_ninja.utils.auth import BasicAuth


def get_token_for_user(user):
    refresh = RefreshToken.for_user(
        user,
    )
    return {
        "refresh_token": str(
            refresh,
        ),
        "access_token": str(
            refresh.access_token,
        ),
        "user": user,
    }


router = Router(
    auth=BasicAuth(),
    tags=["users"],
)


@router.post("login", auth=None, response=TokenSchema | GetUserSchema)
def user_login(request, payload: LoginSchema):
    user = authenticate(request, **payload.dict())
    return get_token_for_user(user)


@router.get("get", response=list[GetUserSchema])
@paginate(PageNumberPagination, page_size=5)
def get_user(request, filters: Query[Filters]):
    return User.objects.all()


@router.post("post", response=UserSchema)
def create_user(request, data: UserSchema):
    request_data = data.dict()
    request_data["password"] = make_password(request_data["password"])
    return User.objects.create(**request_data)


@router.put("put/{int:pk}", response=UserSchema)
def update_user(request, pk: int, data: UserSchema):
    user = get_object_or_404(User, pk=pk)
    for attr, value in data.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


@router.delete("delete/{int:pk}")
def delete_user(request, pk: int):
    employee = get_object_or_404(User, pk=pk)
    employee.delete()
    return {"success": True}
