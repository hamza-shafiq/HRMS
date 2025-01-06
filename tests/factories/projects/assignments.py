import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from projects.models import Assignment
from tests.factories import EmployeeFactory
from tests.factories.projects.projects import ProjectFactory

faker = FakerFactory.create()


@register
class AssignmentFactory(DjangoModelFactory):
    employee = factory.SubFactory(EmployeeFactory)
    project = factory.SubFactory(ProjectFactory)
    start_date = factory.Faker('date_this_year')
    end_date = factory.Faker('date_this_year')
    engagement_type = factory.Faker('random_element', elements=['full_time', 'part_time',
                                                                'contract_based', 'freelance'])

    class Meta:
        model = Assignment
