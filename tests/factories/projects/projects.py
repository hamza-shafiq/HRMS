import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register


faker = FakerFactory.create()


@register
class ProjectFactory(DjangoModelFactory):
    title=factory.faker.Faker("title")
    description=factory.faker.Faker("description")
    added_by=factory.faker.Faker("name")


