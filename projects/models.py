from django.db import models
from employees.models import Employee
from user.models import BaseModel


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, related_name="employee_assignment", on_delete=models.CASCADE, null=True,
                                 blank=True)
    project = models.ForeignKey('Projects', related_name="assignments", on_delete=models.CASCADE, null=True,
                                blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    ENGAGEMENT_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract_based', 'Contract Based'),
        ('freelance', 'Freelance'),
    ]

    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'assignment'


class Projects(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    tech_stack = models.TextField(null=True, blank=True)

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    added_by = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    team_lead = models.ForeignKey(Employee, related_name="team_lead_employee", on_delete=models.CASCADE, null=True,
                                  blank=True)
    account_manager = models.ForeignKey(Employee, related_name="account_manager", on_delete=models.CASCADE, null=True,
                                        blank=True)


    team_members = models.ManyToManyField(Employee, through=Assignment, related_name="projects_assigned", blank=True)

    class Meta:
        db_table = 'projects'
