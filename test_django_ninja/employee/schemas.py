from ninja import ModelSchema
from .models import Employee


class EmployeeSchema(ModelSchema):
    class Meta:
        model = Employee
        fields = "__all__"