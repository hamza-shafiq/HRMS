import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4())
    config = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True


class Department(BaseModel):
    department_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.department_name} {self.id}'


class Employee(BaseModel):
    GENDER_OPTIONS = [
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
        ('OTHER', 'OTHER')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.TextField(max_length=20)
    email = models.EmailField()
    national_id_number = models.IntegerField(null=False, unique=True)
    emergency_contact_number = models.TextField(max_length=20)
    gender = models.CharField(choices=GENDER_OPTIONS, max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    designation = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)
    account_number = models.TextField(max_length=50)
    profile_pic = models.URLField(max_length=200)
    joining_date = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.id}"
