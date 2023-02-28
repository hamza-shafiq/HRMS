import tempfile

from django.urls import reverse
from rest_framework import status

from employees.models import Employee


def temp_file():
    file = tempfile.NamedTemporaryFile(mode='w+b')
    file.write(b'test file')
    file.seek(0)
    return file


def test_retrieve_employee(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.patch(reverse('employees-detail', kwargs={'pk': employee.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(employee.id)


def test_patch_employee(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"national_id_number": '3242'}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('employees-detail', kwargs={'pk': employee.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['national_id_number'] == data['national_id_number']


def test_put_employee(admin_factory, employee_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    department = department_factory()
    file = temp_file()
    data = {
        "first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946, "national_id_number": '2341223488',
        "emergency_contact_number": 934233800, "gender": "MALE", "department": department.id,
        "designation": "Developer", "bank": "Habib", "account_number": 324244, "profile_pic": file,
        "joining_date": "1990-06-20", "employee_status": "WORKING", "username": 'Tayyab123',
        "email": 'usama@gmail.com', "password": "paklove"}

    client = authed_token_client_generator(user)
    response = client.put(reverse('employees-detail', kwargs={'pk': employee.id}), data=data)
    file.close()
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['gender'] == data['gender']


def test_delete_employee(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('employees-detail', kwargs={'pk': employee.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    employee.refresh_from_db()
    assert employee.is_deleted
    assert Employee.global_objects.count() == 1
    assert Employee.deleted_objects.count() == 1
    assert Employee.objects.count() == 0


def test_retrieve_delete_employee_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('employees-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('employees-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_patch_employee_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "national_id_number": '33242'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('employees-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_put_employee_invalid_id(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {"first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946,
            "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "MALE",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
            "employee_status": "WORKING", "username": 'Tayyab123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('employees-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_patch_employee_invalid_choices(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    gender_data = {
        "gender": 'invalid'
    }
    status_data = {
        "employee_status": 'invalid'
    }
    client = authed_token_client_generator(user)
    response1 = client.patch(reverse('employees-detail', kwargs={'pk': employee.id}), data=gender_data, format='json')
    response2 = client.patch(reverse('employees-detail', kwargs={'pk': employee.id}), data=status_data, format='json')
    assert response1.status_code == status.HTTP_400_BAD_REQUEST
    assert response1.json()['gender'][0] == '"invalid" is not a valid choice.'
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.json()['employee_status'][0] == '"invalid" is not a valid choice.'


def test_put_employee_invalid_choices(admin_factory, employee_factory, department_factory,
                                      authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    department = department_factory()
    data = {"first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946,
            "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "invalid",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
            "employee_status": "invalid", "username": 'Tayyab123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('employees-detail', kwargs={'pk': employee.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['gender'][0] == '"invalid" is not a valid choice.'


def test_patch_employee_non_admin(user_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    employee = employee_factory()
    data = {"national_id_number": '3242'}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('employees-detail', kwargs={'pk': employee.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_put_employee_non_admin(user_factory, employee_factory, department_factory, authed_token_client_generator):
    user = user_factory()
    employee = employee_factory()
    department = department_factory()
    data = {"first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946,
            "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "MALE",
            "department": department.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
            "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
            "employee_status": "WORKING", "username": 'Tayyab123', "email": 'usama@gmail.com',
            "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('employees-detail', kwargs={'pk': employee.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_employee_non_admin(user_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('employees-detail', kwargs={'pk': employee.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
