from django.db import models
from django_extensions.db.models import TitleDescriptionModel

from assets.managers import AssetQuerySet
from employees.models import Employee
from user.models import BaseModel


class BaseTitleDescriptionModel(BaseModel, TitleDescriptionModel):
    class Meta:
        abstract = True


class AssetStatus:
    UNASSIGNED = 'unassigned'
    ASSIGNED = 'assigned'
    ASSET_STATUS = ((UNASSIGNED, 'Unassigned'), (ASSIGNED, 'Assigned'))


class Asset(BaseTitleDescriptionModel):
    asset_model = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=50)
    cost = models.FloatField()
    asset_image = models.FileField(upload_to='asset', verbose_name='asset img', default="null")
    status = models.CharField(max_length=20, choices=AssetStatus.ASSET_STATUS, default=AssetStatus.UNASSIGNED)

    objects = AssetQuerySet()

    class Meta:
        db_table = 'assets'

    def __str__(self):
        return f'{self.title} {self.id}'


class AssignedAsset(BaseModel):
    asset = models.ForeignKey(to=Asset, on_delete=models.CASCADE, related_name='assignee')
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE, related_name="assets")

    class Meta:
        db_table = "assigned_assets"

    def __str__(self):
        return f"{self.asset.title} {self.employee.first_name} {self.id}"
