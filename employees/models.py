from django.db import models

from employees.managers import EmployeeQuerySet
from user.models import BaseModel, User


class Department(BaseModel):
    department_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = "departments"

    def __str__(self):
        return f'{self.department_name}'


class Employee(User):
    GENDER_OPTIONS = [
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
        ('OTHER', 'OTHER')
    ]
    STATUS_CHOICES = [
        ('WORKING', 'WORKING'),
        ('RESIGNED', 'RESIGNED'),
        ('FIRED', 'FIRED')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.TextField(max_length=20)
    national_id_number = models.CharField(max_length=50, null=False, unique=True)
    emergency_contact_number = models.TextField(max_length=20)
    gender = models.CharField(choices=GENDER_OPTIONS, max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    designation = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)
    account_number = models.TextField(max_length=50)
    profile_pic = models.FileField(upload_to='images', verbose_name="profile img", blank=True, null=True)
    joining_date = models.DateField()
    employee_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    remaining_leaves = models.IntegerField(default=18, null=True)
    total_leaves = models.IntegerField(default=18)
    extra_leaves = models.IntegerField(default=0)

    objects = EmployeeQuerySet()

    @property
    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())).strip()
        return self.user.email

    class Meta:
        db_table = "employees"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeHistory(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    subject = models.CharField(max_length=255)
    remarks = models.TextField(max_length=500)
    increment = models.FloatField(default=0)
    interval_from = models.DateField()
    interval_to = models.DateField()
    review_by = models.ForeignKey(Employee, related_name='review_by', on_delete=models.SET_NULL, null=True)
    review_date = models.DateField()
    added_by = models.ForeignKey(Employee, related_name='added_by', on_delete=models.SET_NULL, null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "employee_history"
