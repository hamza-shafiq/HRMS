from django.db import models

from employees.models import Employee
from user.models import BaseModel


class Recruits(BaseModel):
    CHOICES = [
        ('IN_PROCESS', 'IN_PROCESS'),
        ('SCHEDULED', 'SCHEDULED'),
        ('PENDING', 'PENDING'),
        ('SELECTED', 'SELECTED'),
        ('REJECTED', 'REJECTED')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.TextField(max_length=20)
    position = models.CharField(max_length=30)
    # resume = models.URLField(max_length=200)
    resume = models.FileField(upload_to='media', verbose_name="resume pdf")
    status = models.CharField(max_length=100, choices=CHOICES)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    interview_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "recruits"

    @property
    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())).strip()
        return self.email

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __unicode__(self):
        return self.resume


class Referrals(BaseModel):
    recruit = models.ForeignKey(Recruits, on_delete=models.CASCADE, related_name="referrers")
    referer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='recruits_referred', null=True)

    class Meta:
        unique_together = ('recruit', 'referer')
        db_table = "referrals"

    def __str__(self):
        return f'{self.referer.first_name} {self.referer.last_name}'


class RecruitsHistory(BaseModel):
    recruit = models.ForeignKey(Recruits, on_delete=models.CASCADE, related_name="recruit")
    process_stage = models.CharField(max_length=255)
    remarks = models.TextField(max_length=20)
    event_date = models.DateField()
    conduct_by = models.ForeignKey(Employee, related_name='conduct_by', on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(Employee, related_name='recruit_history_added_by',
                                 on_delete=models.SET_NULL, null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "recruit_history"
