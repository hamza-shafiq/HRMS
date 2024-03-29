from django.db import models

from employees.models import Employee
from user.models import BaseModel


class Announcements(BaseModel):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    added_by = models.ForeignKey(Employee, related_name='announcement_added_by', on_delete=models.SET_NULL, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)

    class Meta:
        db_table = "announcements"
