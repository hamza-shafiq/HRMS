from django.urls import reverse
from rest_framework import status


def test_fetch_employees_employees(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-assets', kwargs={'pk': asset.employee.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(employee.id)


def test_fetch_employees_employees_non_existing_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-assets', kwargs={'pk': str(user.id)}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'employees with this id does not exist'


def test_fetch_employees_employees_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-assets', kwargs={'pk': 'invalid'}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Invalid employees id'
