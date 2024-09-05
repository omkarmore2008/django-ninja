from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from test_django_ninja.users.models import User
from test_django_ninja.users.schemas import UserSchema, GetUserSchema, Error, Filters, LoginSchema, TokenSchema
from typing import List
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
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
        "user": user
    }


router = Router(
            auth=BasicAuth(),
            tags=["users"]
        )


@router.post("login", auth=None, response=TokenSchema | GetUserSchema)
def login(request, payload: LoginSchema):
    user = authenticate(request, **payload.dict())    
    return get_token_for_user(user)

@router.get("get", response = List[GetUserSchema])
@paginate(PageNumberPagination, page_size=5)
def get_user(request, filters: Query[Filters]):
    print(request.user.username, ":::::::::::::::")
    user_list = User.objects.all()
    return user_list

@router.post("post", response=UserSchema)
def create_user(request, data: UserSchema):
    request_data = data.dict()
    request_data["password"] = make_password(request_data["password"])
    user = User.objects.create(**request_data)
    return user

@router.put("put/{int:id}", response=UserSchema)
def update_user(request, id: int, data: UserSchema):
    user = get_object_or_404(User, pk=id)
    for attr, value in data.dict().items():
        setattr(user, attr, value)
    user.save()
    return user

@router.delete("delete/{int:id}")
def delete_employee(request, id: int):
    employee = get_object_or_404(User, pk=id)
    employee.delete()
    return {"success": True}
