import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class AdminFactory(DjangoModelFactory):
    username = factory.LazyAttribute(lambda a: 'admin'.lower())
    email = factory.LazyAttribute(lambda a: '{}@admin.com'.format(a.username).lower())
    is_active = True
    is_staff = True
    is_verified = True
    is_admin = True

    class Meta:
        model = 'user.User'

    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            self.set_password(extracted)


@register
class UserFactory(DjangoModelFactory):
    username = factory.LazyAttribute(lambda a: 'user')
    email = factory.LazyAttribute(lambda a: '{}@example.com'.format(a.username))
    is_active = True
    is_verified = True
    is_superuser = False
    is_employee = True
    is_staff = False

    class Meta:
        model = 'user.User'

    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            self.set_password(extracted)
