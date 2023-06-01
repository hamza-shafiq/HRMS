from django.db import models
from employees.models import Employee
from user.models import BaseModel


class Payroll(BaseModel):
    MONTH_OPTIONS = [
        ('JANUARY', 'JANUARY'),
        ('FEBRUARY', 'FEBRUARY'),
        ('MARCH', 'MARCH'),
        ('APRIL', 'APRIL'),
        ('MAY', 'MAY'),
        ('JUNE', 'JUNE'),
        ('JULY', 'JULY'),
        ('AUGUST', 'AUGUST'),
        ('SEPTEMBER', 'SEPTEMBER'),
        ('OCTOBER', 'OCTOBER'),
        ('NOVEMBER', 'NOVEMBER'),
        ('DECEMBER', 'DECEMBER'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    basic_salary = models.FloatField()
    bonus = models.FloatField(default=0)
    reimbursement = models.FloatField(default=0)
    travel_allowance = models.FloatField(default=0)
    tax_deduction = models.FloatField(default=0)
    month = models.CharField(max_length=20, choices=MONTH_OPTIONS)
    year = models.CharField(max_length=50)
    released = models.BooleanField(default=False)

    class Meta:
        db_table = "payrolls"

    def __str__(self):
        return f"{self.employee.first_name + ' ' + self.employee.last_name}"
