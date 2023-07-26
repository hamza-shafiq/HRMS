import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from .department import DepartmentFactory

faker = FakerFactory.create()


@register
class EmployeeFactory(DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda a: '{0}.{1}example.com'.format(a.first_name, a.last_name).lower())
    email = factory.LazyAttribute(lambda a: '{}@example.com'.format(a.username))
    phone_number = factory.Sequence(lambda x: '12345{}'.format(x))
    national_id_number = factory.Sequence(lambda x: '12345{}'.format(x))
    emergency_contact_number = factory.Sequence(lambda x: '23532526')
    gender = factory.Sequence(lambda x: 'MALE')
    department = factory.SubFactory(DepartmentFactory)
    designation = factory.Sequence(lambda x: 'Developer{}'.format(x))
    bank = factory.Sequence(lambda x: 'Faisal{}'.format(x))
    account_number = factory.Sequence(lambda x: x)
    profile_pic = factory.Sequence(lambda x: 'http://google.com')
    joining_date = factory.Sequence(lambda x: '2022-07-06')
    employee_status = factory.Sequence(lambda x: 'WORKING')
    is_verified = factory.Sequence(lambda x: True)

    class Meta:
        model = 'employees.Employee'
