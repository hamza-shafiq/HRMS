import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status


def test_filter_employees(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-employee-detail') + "?employee_id=" + str(employee.id))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(employee.id)


def test_filter_employees_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    with pytest.raises(ValidationError) as e:
        client.get(reverse('employees-employee-detail') + "?employee_id=" + str('invalid'))
    assert e.value.message == 'Invalid employee id'


def test_filter_non_existing_employee(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-employee-detail') + "?employee_id=" + str(user.id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['error'] == f'Employee with id: {user.id} does not exist'


def test_filter_with_empty_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-employee-detail'))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_filter_employee_own_detail(employee_factory, authed_token_client_generator):
    user = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-employee-detail'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(user.id)


def test_filter_employee_with_user(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-employee-detail'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
