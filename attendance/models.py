from django.db import models
from employees.models import Employee, BaseModel


class Attendance(BaseModel):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id.first_name} {self.date}"


class Leaves(BaseModel):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    reason = models.TextField(max_length=500)
    request_date = models.DateTimeField()

    def __str__(self):
        return f"{self.employee_id.first_name} {self.request_date}"
