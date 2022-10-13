from django.urls import reverse
from rest_framework import status


def test_retrieve_attendance(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_200_OK


def test_patch_attendance(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == data['status']


def test_put_attendance(admin_factory, attendance_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == data['status']


def test_delete_attendance(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_retrieve_delete_attendance_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('attendance-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('attendance-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_attendance_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "national_id_number": '33242'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_attendance_invalid_id(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {
        "first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946, "national_id_number": '2341223488',
        "emergency_contact_number": 934233800, "gender": "MALE", "employee": employee.id, "designation": "Developer",
        "bank": "Habib", "account_number": 324244, "profile_pic": "http://asfasf.asd",
        "joining_date": "1990-06-20 08:03", "attendance_status": "WORKING", "username": 'Tayyab123',
        "email": 'usama@gmail.com', "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_attendance_invalid_choices(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    gender_data = {
        "gender": 'invalid'
    }
    status_data = {
        "attendance_status": 'invalid'
    }
    client = authed_token_client_generator(user)
    response1 = client.patch(reverse('attendance-detail',
                                     kwargs={'pk': attendance.id}), data=gender_data, format='json')
    response2 = client.patch(reverse('attendance-detail',
                                     kwargs={'pk': attendance.id}), data=status_data, format='json')
    assert response1.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.status_code == status.HTTP_400_BAD_REQUEST


def test_put_attendance_invalid_choices(admin_factory, attendance_factory, employee_factory,
                                        authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    employee = employee_factory()
    data = {
        "first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946,
        "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "invalid",
        "employee": employee.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
        "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03", "attendance_status": "invalid",
        "username": 'Tayyab123', "email": 'usama@gmail.com', "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_attendance_non_admin(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    data = {
        "national_id_number": '3242'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_put_attendance_non_admin(user_factory, attendance_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    employee = employee_factory()

    data = {
        "first_name": 'Kamran', "last_name": 'Babar', "phone_number": +92304636946,
        "national_id_number": '2341223488', "emergency_contact_number": 934233800, "gender": "MALE",
        "employee": employee.id, "designation": "Developer", "bank": "Habib", "account_number": 324244,
        "profile_pic": "http://asfasf.asd", "joining_date": "1990-06-20 08:03",
        "attendance_status": "WORKING", "username": 'Tayyab123', "email": 'usama@gmail.com',
        "password": "paklove"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_attendance_non_admin(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
