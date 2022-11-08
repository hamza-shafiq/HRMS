from django.urls import reverse
from rest_framework import status


def test_filter_recruits(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruits = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list') + "?recruit_id=" + str(recruits.id))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(recruits.id)


def test_filter_recruits_does_not_exist(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list') + "?recruit_id=" + str(user.id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['error'] == f'Recruit with id: {user.id} does not exist'


def test_filter_recruits_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list') + "?recruit_id=" + str('invalid'))
    assert response.json()['detail'] == 'Invalid Recruit id'
