from django.db import models
from model_utils import FieldTracker

from employees.models import Employee
from user.models import BaseModel


class Attendance(BaseModel):
    STATUS_CHOICE = [
        ('LATE_ARRIVAL', 'LATE_ARRIVAL'),
        ('EARLY_ARRIVAL', 'EARLY_ARRIVAL'),
        ('EARLY_DEPARTURE', 'EARLY_DEPARTURE'),
        ('LATE_DEPARTURE', 'LATE_DEPARTURE'),
        ('ON_TIME', 'ON_TIME'),
        ('ATTENDANCE_REQUEST', 'ATTENDANCE_REQUEST'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    total_time = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

    class Meta:
        db_table = "attendances"

    def __str__(self):
        return f"{self.employee.first_name} {self.created}"


class Leaves(BaseModel):
    STATUS_CHOICE = [
        ('PENDING', 'PENDING'),
        ('REJECTED', 'REJECTED'),
        ('APPROVED', 'APPROVED'),
    ]

    LEAVE_CHOICES = [
        ('SICK_LEAVE', 'SICK_LEAVE'),
        ('CASUAL_LEAVE', 'CASUAL_LEAVE'),
        ('MATERNITY_LEAVE', 'MATERNITY_LEAVE'),
        ('PATERNITY_LEAVE', 'PATERNITY_LEAVE'),
        ('MARRIAGE_LEAVE', 'MARRIAGE_LEAVE'),
        ('EMERGENCY_LEAVE', 'EMERGENCY_LEAVE'),
        ('WORK_FROM_HOME', 'WORK_FROM_HOME'),
        ('EXTRA_DAYS', 'EXTRA_DAYS'),
        ('REIMBURSEMENT','REIMBURSEMENT'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=50, choices=LEAVE_CHOICES)
    reason = models.TextField(max_length=500)
    request_date = models.DateTimeField()
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(default='PENDING', max_length=50, choices=STATUS_CHOICE)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name="approved_by")
    tracker = FieldTracker(fields=['status'])

    class Meta:
        db_table = "leaves"

    def __str__(self):
        return f"{self.employee.first_name} {self.created}"


class AttendanceRequest(models.Model):
    CHECK_TYPE_CHOICES = [
        ('CHECK_IN', 'Check In'),
        ('CHECK_OUT', 'Check Out'),
        ('CHECK_IN_CHECK_OUT', 'Check In and Check Out'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_requests")
    check_type = models.CharField(max_length=20, choices=CHECK_TYPE_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)
    attendance_date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.TextField(max_length=500)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="request_approver")
    tracker = FieldTracker(fields=['status'])

    class Meta:
        db_table = "attendance_requests"

    def __str__(self):
        return f"{self.employee.first_name} - {self.attendance_date} - {self.check_type}"
