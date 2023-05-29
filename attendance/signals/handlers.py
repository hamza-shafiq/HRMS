from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save

from attendance.models import Leaves


def difference_date(from_date, to_date):
    date1 = datetime.strptime(from_date, '%Y-%m-%d')
    date2 = datetime.strptime(to_date, '%Y-%m-%d')

    delta = date2 - date1
    return delta.days

@receiver(post_save, sender=Leaves)
def update_employee_leaves(sender, instance, created, **kwargs):
    if not created and instance.status == "APPROVED":
        remaining_leaves = instance.employee.remaining_leaves
        applied_leaves = difference_date(str(instance.from_date), str(instance.to_date))
        remaining_leaves = remaining_leaves - applied_leaves
        instance.employee.remaining_leaves = remaining_leaves - 1
        instance.employee.save()

