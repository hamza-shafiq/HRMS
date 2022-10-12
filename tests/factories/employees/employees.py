import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from .department import DepartmentFactory
faker = FakerFactory.create()


@register
class EmployeeFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda x: 'f_name{}'.format(x))
    last_name = factory.Sequence(lambda x: 'l_name{}'.format(x))
    phone_number = factory.Sequence(lambda x: '12345'.format(x))
    national_id_number = factory.Sequence(lambda x: '4353553'.format(x))
    emergency_contact_number = factory.Sequence(lambda x: '23532526'.format(x))
    gender = factory.Sequence(lambda x: 'MALE'.format(x))
    department = factory.SubFactory(DepartmentFactory)
    designation = factory.Sequence(lambda x: 'Developer{}'.format(x))
    bank = factory.Sequence(lambda x: 'Faisal{}'.format(x))
    account_number = factory.Sequence(lambda x: x)
    profile_pic = factory.Sequence(lambda x: 'http://google.com'.format(x))
    joining_date = factory.Sequence(lambda x: '2022-07-06'.format(x))
    employee_status = factory.Sequence(lambda x: 'WORKING'.format(x))
    is_verified = factory.Sequence(lambda x: True)

    class Meta:
        model = 'employees.Employee'
