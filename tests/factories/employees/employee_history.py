import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from .employees import EmployeeFactory

faker = FakerFactory.create()


@register
class EmployeeHistoryFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    increment = 100.00
    interval_from = factory.Sequence(lambda x: "2024-01-01")
    interval_to = factory.Sequence(lambda x: "2024-01-31")
    review_by = factory.SubFactory(EmployeeFactory)
    review_date = factory.Sequence(lambda x: "2024-02-01")
    added_by = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = 'employees.EmployeeHistory'
