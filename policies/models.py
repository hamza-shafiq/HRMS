from django.db import models

from employees.models import Employee
from user.models import BaseModel


class Policies(BaseModel):
    file_name = models.CharField(max_length=100)
    policy_file = models.FileField(upload_to='media', verbose_name="policy_pdf")
    modified_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="policies")

    class Meta:
        db_table = "policies"

    def __unicode__(self):
        return self.policy_file
