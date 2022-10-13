from django.urls import reverse
from rest_framework import status
from employees.models import Department


def test_get_department(user_factory, department_factory, authed_token_client_generator):
    user = user_factory()
    department = department_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-list'))
    assert response.json()[0]['department_name'] == department.department_name
    assert response.status_code == status.HTTP_200_OK


def test_create_department(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"department_name": "python_department", "description": "test_description"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('department-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['department_name'] == data['department_name']


def test_create_department_invalid_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"department_name": '', "description": "test_description"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('department-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_department_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {"department_name": 'Backend', "description": "test_description"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('department-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_department_count(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-list'))
    assert len(response.json()) == Department.objects.all().count()
