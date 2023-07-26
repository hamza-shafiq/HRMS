import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

faker = FakerFactory.create()


@register
class RecruitFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda x: 'last_name{}'.format(x))
    last_name = factory.Sequence(lambda x: 'first_name{}'.format(x))
    email = factory.Sequence(lambda x: 'user@gmail.com')
    phone_number = factory.Sequence(lambda x: '030463600')
    position = factory.Sequence(lambda x: 'Developer')
    resume = factory.Sequence(lambda x: 'git.pdf')
    status = factory.Sequence(lambda x: 'IN_PROCESS')

    class Meta:
        model = 'recruitments.Recruits'
