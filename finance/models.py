from django.db import models
from employees.models import Employee
from user.models import BaseModel


class Payroll(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payroll")
    basic_salary = models.FloatField()
    bonus = models.FloatField()
    reimbursement = models.FloatField()
    travel_allowance = models.FloatField()
    tax_deduction = models.FloatField()
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=50)
    released = models.BooleanField()

    def __str__(self):
        return f"{self.employee.first_name}"
