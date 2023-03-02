from django.urls import reverse
from rest_framework import status


def test_filter_recruits(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruits = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list') + "?position=" + str(recruits.position))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['position'] == str(recruits.position)
