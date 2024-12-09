from django.db import models
from django.conf import settings

from employees.models import Employee
from user.models import BaseModel


class Projects(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.TextField()
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    added_by = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ManyToManyField(Employee, related_name="Assignment")


    class Meta:
        db_table = 'projects'