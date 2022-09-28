from django.db import models
from employees.models import Employee, BaseModel
from django_extensions.db.models import TitleDescriptionModel


class BaseTitleDescriptionModel(BaseModel, TitleDescriptionModel):
    class Meta:
        abstract = True


class Asset(BaseTitleDescriptionModel):
    asset_model = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=50)
    cost = models.FloatField()

    def __str__(self):
        return f'{self.title} {self.id}'


class AssignedAsset(BaseModel, ):
    asset = models.ForeignKey(to=Asset, on_delete=models.CASCADE, related_name='assignee')
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE, related_name="assets")

    def __str__(self):
        return f"{self.asset.title} {self.employee.first_name} {self.id}"
