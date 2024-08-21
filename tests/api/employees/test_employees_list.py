import tempfile

from django.urls import reverse
from rest_framework import status

from employees.models import Employee


def temp_file():
    file = tempfile.NamedTemporaryFile(mode='w+b')
    file.write(b'test file')
    file.seek(0)
    return file


def test_get_employees(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['national_id_number'] == employee.national_id_number


def test_create_employees(admin_factory, department_factory, authed_token_client_generator, celery_eager_run_on_commit,
                          mailoutbox):
    user = admin_factory()
    department = department_factory()
    file = temp_file()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800, "national_id_number": 33,
            "emergency_contact_number": 934233800, "gender": "MALE", "department": department.id,
            "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": file, "joining_date": "1990-06-20", "employee_status": "WORKING", 'total_leaves': 17,
            "username": 'usama123', "email": 'usama@gmail.com', "password": "paklove", 'is_verified': True,
            "is_active": True}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    file.close()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['username'] == data['username']
    assert response.json()['total_leaves'] == data['total_leaves']
    assert response.json()['remaining_leaves'] == data['total_leaves']


def test_create_employees_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"first_name": 324, "last_name": "jamal"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['username'][0] == 'This field is required.'


def test_get_employees_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_employees_non_admin_team_lead(employee_factory, authed_token_client_generator):
    teamlead = employee_factory(is_team_lead=True)
    employee = employee_factory(team_lead=teamlead)
    client = authed_token_client_generator(teamlead)
    response = client.get(reverse('employees-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['national_id_number'] == employee.national_id_number


def test_create_employees_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
        "first_name": 'usama',
        "last_name": "jamal",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_create_employees_invalid_status(admin_factory, department_factory, authed_token_client_generator,
                                         celery_eager_run_on_commit, mailoutbox):
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
    assert response.json()['employee_status'][0] == '"invalid" is not a valid choice.'


def test_create_employees_invalid_gender(admin_factory, department_factory, authed_token_client_generator,
                                         celery_eager_run_on_commit, mailoutbox):
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
    assert response.json()['gender'][0] == '"invalid" is not a valid choice.'


def test_unique_constraint_employees(admin_factory, department_factory, authed_token_client_generator,
                                     celery_eager_run_on_commit, mailoutbox):
    user = admin_factory()
    department = department_factory()
    file = temp_file()
    data = {"first_name": 'Usama', "last_name": 'Tariq', "phone_number": +923046369800,
            "national_id_number": 33, "emergency_contact_number": 934233800, "gender": "MALE",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": file, "joining_date": "1990-06-20",
            "employee_status": "WORKING", "username": 'usama123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    client.post(reverse('employees-list'), data=data)
    response = client.post(reverse('employees-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    file.close()
    assert response.json()['username'][0] == 'Username already exists.'
    assert response.json()['email'][0] == 'user with this email already exists.'


def test_get_employees_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employees-list'))
    assert response.json()['count'] == Employee.objects.all().count()
