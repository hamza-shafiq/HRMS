from django.db import models
from employees.models import Employee, BaseModel


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
    position = models.CharField(max_length=20)
    resume = models.URLField(max_length=200)
    status = models.CharField(max_length=100, choices=CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Referrals(BaseModel):
    recruit = models.ForeignKey(Recruits, on_delete=models.CASCADE, related_name="referrals")
    referer = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recruit', 'referer')

    def __str__(self):
        return f'{self.recruit.first_name} {self.referer.first_name}'
