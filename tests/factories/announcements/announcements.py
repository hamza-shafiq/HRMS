import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from ..employees import EmployeeFactory

faker = FakerFactory.create()


@register
class AnnouncementFactory(DjangoModelFactory):
    title = factory.Sequence(lambda x: 'title{}'.format(x))
    detail = factory.Sequence(lambda x: 'detail{}'.format(x))
    date_from = factory.Sequence(lambda x: "2024-01-01")
    date_to = factory.Sequence(lambda x: "2024-01-31")
    added_by = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = 'announcements.Announcements'
