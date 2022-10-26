import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from tests.factories.employees.employees import EmployeeFactory

from .asset import AssetFactory

faker = FakerFactory.create()


@register
class AssigneeFactory(DjangoModelFactory):
    asset = factory.SubFactory(AssetFactory)
    employee = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = 'assets.AssignedAsset'
