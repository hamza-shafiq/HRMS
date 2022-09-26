from django.db import models
from employees.models import Employee, BaseModel


class Asset(BaseModel):
    name = models.CharField(max_length=50)
    asset_model = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    is_deleted = models.BooleanField()

    def __str__(self):
        return f'{self.name}'


class AssignedAsset(BaseModel):
    asset_name = models.ForeignKey(to=Asset, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(to=Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.asset_name.name} {self.employee_id.first_name}"
