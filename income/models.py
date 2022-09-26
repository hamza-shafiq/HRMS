from django.db import models
from employees.models import Employee, BaseModel


class Payroll(BaseModel):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.IntegerField()
    bonus = models.IntegerField()
    reimbursement = models.IntegerField()
    travel_allowance = models.IntegerField()
    tax_deduction = models.IntegerField()
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=50)
    released = models.BooleanField()

    def __str__(self):
        return f"{self.employee_id.first_name}"
