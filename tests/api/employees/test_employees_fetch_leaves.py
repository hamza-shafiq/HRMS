from django.urls import reverse
from rest_framework import status


def test_fetch_employee_leaves(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-leaves', kwargs={'pk': leave.employee.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(leave.id)


def test_fetch_employee_leaves_non_existing_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-leaves', kwargs={'pk': user.id}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Employee with this id does not exist'


def test_fetch_employee_leaves_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-leaves', kwargs={'pk': 'invalid'}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Invalid employee id'


def test_fetch_employee_leaves(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-leaves', kwargs={'pk': 'anything'}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
