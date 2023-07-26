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
    response = client.get(reverse('employees-employee-detail') + "?employee_id=" + str('invalid'))
    assert response.json()['detail'] == 'Invalid employee id'


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


def test_filter_employees_status(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory(employee_status='WORKING')
    employee_factory(employee_status='RESIGNED')
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list') + "?employee_status=" + str(employee1.employee_status))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['id'] == str(employee1.id)


def test_filter_employees_department(admin_factory, employee_factory, department_factory,
                                     authed_token_client_generator):
    user = admin_factory()
    dep1 = department_factory()
    dep2 = department_factory()
    employee1 = employee_factory(department=dep1)
    employee_factory(department=dep2)
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list') + "?department=" + str(dep1.id))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['id'] == str(employee1.id)
