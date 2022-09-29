from django.db import models
from employees.models import Employee, BaseModel


class Attendance(BaseModel):
    STATUS_CHOICE = [
        ('LATE_ARRIVAL', 'LATE_ARRIVAL'),
        ('EARLY_ARRIVAL', 'EARLY_ARRIVAL'),
        ('EARLY_DEPARTURE', 'EARLY_DEPARTURE'),
        ('LATE_DEPARTURE', 'LATE_DEPARTURE'),
        ('ON_TIME', 'ON_TIME')
    ]
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

    def __str__(self):
        return f"{self.employee_id.first_name} {self.date}"


class Leaves(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=50)
    reason = models.TextField(max_length=500)
    request_date = models.DateTimeField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f"{self.employee.first_name} {self.request_date}"
