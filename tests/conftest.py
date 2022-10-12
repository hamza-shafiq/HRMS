import pytest
from factories import *  # noqa
from pytest_django.lazy_django import skip_if_no_django


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def rest_client():
    """A Django Rest Framework api test client instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
def user_token_generator():
    def _user_token_generator(user):
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken.for_user(user)
        return token.access_token
    return _user_token_generator


@pytest.fixture()
def authed_token_client_generator(rest_client, user_token_generator):

    def _client_generator(user):
        token = user_token_generator(user)

        rest_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(str(token)))
        return rest_client

    return _client_generator
