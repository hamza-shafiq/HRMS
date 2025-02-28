import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from projects.models import Projects
from tests.factories import EmployeeFactory

faker = FakerFactory.create()


@register
class ProjectFactory(DjangoModelFactory):
    title = factory.Faker('word')
    description = factory.Faker('paragraph')
    tech_stack = factory.Faker('sentence')
    status = factory.Faker('random_element', elements=['not_started', 'in_progress',
                                                       'completed', 'on_hold', 'canceled'])
    added_by = factory.Faker('name')
    start_date = factory.Faker('date_this_decade')
    end_date = factory.Faker('date_this_decade')
    team_lead = factory.SubFactory(EmployeeFactory)
    account_manager = factory.SubFactory(EmployeeFactory)

    class Meta:
        model = Projects
