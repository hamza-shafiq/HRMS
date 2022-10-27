from django.urls import reverse
from rest_framework import status

from employees.models import Employee


def test_get_employees(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['national_id_number'] == employee.national_id_number


def test_create_employees(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800, "national_id_number": 33,
            "emergency_contact_number": 934233800, "gender": "MALE", "department": department.id,
            "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03", "employee_status": "WORKING",
            "username": 'usama123', "email": 'usama@gmail.com', "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['username'] == data['username']


def test_create_employees_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"first_name": 324, "last_name": "jamal"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_employees_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_employees_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
        "first_name": 'usama',
        "last_name": "jamal",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_employees_invalid_status(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800,
            "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "MALE",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03", "employee_status": "invalid",
            "username": 'usama123', "email": 'usama@gmail.com', "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_employees_invalid_gender(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800,
            "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "invalid",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
            "employee_status": "WORKING", "username": 'usama123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unique_constraint_employees(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800,
            "national_id_number": 33, "emergency_contact_number": 934233800, "gender": "MALE",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
            "employee_status": "WORKING", "username": 'usama123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    client.post(reverse('employees-list'), data=data)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_employees_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert len(response.json()) == Employee.objects.all().count()
