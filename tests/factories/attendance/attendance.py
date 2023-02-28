import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees.employees import EmployeeFactory

faker = FakerFactory.create()


@register
class AttendanceFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    check_in = factory.Sequence(lambda x: '2022-07-06 12:12:12.05+00:00')
    check_out = factory.Sequence(lambda x: '2022-07-06 12:12:12.05+00:00')
    status = factory.Sequence(lambda x: 'ON_TIME')

    class Meta:
        model = 'attendance.Attendance'
