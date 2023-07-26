import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

faker = FakerFactory.create()


@register
class DepartmentFactory(DjangoModelFactory):
    department_name = factory.Sequence(lambda x: 'department{}'.format(x))
    description = factory.Sequence(lambda x: 'description{}'.format(x))

    class Meta:
        model = 'employees.Department'
