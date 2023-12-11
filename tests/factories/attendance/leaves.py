import datetime

import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees.employees import EmployeeFactory

faker = FakerFactory.create()


@register
class LeavesFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    reason = factory.Sequence(lambda x: 'urgent_work')
    leave_type = factory.Sequence(lambda x: 'casual')
    request_date = factory.Sequence(lambda x: str(datetime.datetime.now().date()))
    from_date = factory.Sequence(lambda x: str(datetime.datetime.now().date()))
    to_date = factory.Sequence(lambda x: str((datetime.datetime.now() + datetime.timedelta(days=1)).date()))

    class Meta:
        model = 'attendance.Leaves'
