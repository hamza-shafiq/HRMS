from django.urls import reverse
from rest_framework import status


def test_fetch_department_employees(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-employees', kwargs={'pk': employee.department.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(employee.id)


def test_fetch_department_employees_non_existing_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-employees', kwargs={'pk': str(user.id)}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Department with this id does not exist'


def test_fetch_department_employees_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-employees', kwargs={'pk': 'invalid'}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Invalid department id'


def test_fetch_department_employees_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-employees', kwargs={'pk': 'anything'}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
