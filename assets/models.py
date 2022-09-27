from django.db import models
from employees.models import Employee, BaseModel


class Asset(BaseModel):
    asset_name = models.CharField(max_length=50)
    asset_model = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=50)
    asset_description = models.CharField(max_length=250)
    cost = models.FloatField
    is_deleted = models.BooleanField()

    def __str__(self):
        return f'{self.asset_name} {self.id}'


class AssignedAsset(BaseModel):
    asset = models.ForeignKey(to=Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE, related_name="assigned_asset")

    def __str__(self):
        return f"{self.asset.asset_name} {self.employee.first_name} {self.id}"
