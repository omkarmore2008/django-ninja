from django.shortcuts import get_object_or_404
from ninja import Query
from ninja import Router
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from test_django_ninja.employee.models import Employee
from test_django_ninja.employee.schemas import EmployeeSchema
from test_django_ninja.users.schemas import Filters
from test_django_ninja.utils.auth import BasicAuth

router = Router(
    auth=BasicAuth(),
    tags=["employee"],
)


@router.get("get", response=list[EmployeeSchema])
@paginate(PageNumberPagination, page_size=5)
def get_employee(request, filters: Query[Filters]):
    return Employee.objects.all()


@router.post("post", response=EmployeeSchema)
def create_employee(request, data: EmployeeSchema):
    return Employee.objects.create(**data.dict())


@router.put("put/{int:pk}", response=EmployeeSchema)
def update_employee(request, pk: int, data: EmployeeSchema):
    user = get_object_or_404(Employee, pk=pk)
    for attr, value in data.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


@router.delete("delete/{int:pk}")
def delete_employee(request, pk: int):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return {"success": True}
