from django.db import models
from user.models import BaseModel


class Policies(BaseModel):
    file_name = models.CharField(max_length=100)
    policy_file = models.FileField(upload_to='media', verbose_name="resume pdf")

    class Meta:
        db_table = "policies"

    def __unicode__(self):
        return self.policy_file
