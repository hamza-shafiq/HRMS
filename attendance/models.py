from django.db import models
from employees.models import Employee
from user.models import BaseModel


class Attendance(BaseModel):
    STATUS_CHOICE = [
        ('LATE_ARRIVAL', 'LATE_ARRIVAL'),
        ('EARLY_ARRIVAL', 'EARLY_ARRIVAL'),
        ('EARLY_DEPARTURE', 'EARLY_DEPARTURE'),
        ('LATE_DEPARTURE', 'LATE_DEPARTURE'),
        ('ON_TIME', 'ON_TIME')
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

    def __str__(self):
        return f"{self.employee.first_name} {self.created}"


class Leaves(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=50)
    reason = models.TextField(max_length=500)
    request_date = models.DateTimeField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f"{self.employee.first_name} {self.created}"
