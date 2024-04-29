from django.db import models

from employees.models import Employee
from user.models import BaseModel


class Tasks(BaseModel):
    STATUS_CHOICE = [
        ('NOT_STARTED', 'NOT_STARTED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('DONE', 'DONE'),
        ('BLOCKED', 'BLOCKED'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_by = models.ForeignKey(Employee, related_name='tasks_assigned_by', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, related_name='assigned_to', on_delete=models.SET_NULL, null=True)
    deadline = models.DateField()
    status = models.CharField(default='NOT_STARTED', max_length=50, choices=STATUS_CHOICE)

    class Meta:
        db_table = "tasks"
