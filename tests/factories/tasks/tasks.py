import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees import EmployeeFactory

faker = FakerFactory.create()


@register
class TaskFactory(DjangoModelFactory):
    title = factory.Sequence(lambda x: 'title{}'.format(x))
    description = factory.Sequence(lambda x: 'description{}'.format(x))
    status = factory.Sequence(lambda x: 'done')
    deadline = factory.Sequence(lambda x: "2024-01-01")
    employee = factory.SubFactory(EmployeeFactory)
    assigned_by = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = 'tasks.tasks'
