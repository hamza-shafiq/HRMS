import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from employees.models import Tenure
from pytest_factoryboy import register

from .employees import EmployeeFactory

faker = FakerFactory.create()


@register
class TenureFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    interval_from = factory.Sequence(lambda x: "2024-01-01")
    interval_to = factory.Sequence(lambda x: "2024-01-31")
    allocated_leaves = 16
    added_by = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = Tenure