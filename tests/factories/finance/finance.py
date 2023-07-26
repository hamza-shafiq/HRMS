import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees.employees import EmployeeFactory

faker = FakerFactory.create()


@register
class PayrollFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    basic_salary = 2000
    month = factory.Sequence(lambda x: 'MAY')
    year = factory.Sequence(lambda x: '2022')
    released = False

    class Meta:
        model = 'finance.Payroll'
