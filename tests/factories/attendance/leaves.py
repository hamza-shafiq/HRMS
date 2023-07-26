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
    request_date = factory.Sequence(lambda x: '2022-07-06')
    from_date = factory.Sequence(lambda x: '2022-07-06')
    to_date = factory.Sequence(lambda x: '2022-07-06')

    class Meta:
        model = 'attendance.Leaves'
