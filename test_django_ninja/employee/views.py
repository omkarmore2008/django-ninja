from django.shortcuts import render, get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination

from typing import List
from test_django_ninja.utils.auth import BasicAuth
from .models import Employee
from .schemas import EmployeeSchema
from ..users.schemas import Filters

router = Router(
            auth=BasicAuth(),
            tags=["employee"]
)


@router.get("get", response = List[EmployeeSchema])
@paginate(PageNumberPagination, page_size=5)
def get_employee(request, filters: Query[Filters]):
    user_list = Employee.objects.all()
    return user_list

@router.post("post", response=EmployeeSchema)
def create_employee(request, data: EmployeeSchema):
    user = Employee.objects.create(**data.dict())
    return user

@router.put("put/{int:id}", response=EmployeeSchema)
def update_employee(request, id: int, data: EmployeeSchema):
    user = get_object_or_404(Employee, pk=id)
    for attr, value in data.dict().items():
        setattr(user, attr, value)
    user.save()
    return user

@router.delete("delete/{int:id}")
def delete_employee(request, id: int):
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()
    return {"success": True}
