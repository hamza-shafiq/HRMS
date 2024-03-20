import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees import EmployeeFactory
from .recruits import RecruitFactory

faker = FakerFactory.create()


@register
class RecruitsHistoryFactory(DjangoModelFactory):
    recruit = factory.SubFactory(RecruitFactory)
    event_date = factory.Sequence(lambda x: "2024-01-31")
    conduct_by = factory.SubFactory(EmployeeFactory)
    added_by = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = 'recruitments.RecruitsHistory'
