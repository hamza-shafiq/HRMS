from django.urls import reverse
from rest_framework import status


def test_retrieve_attendance(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_200_OK


def test_retrieve_attendance_employee(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
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
        "status": 'EARLY_ARRIVAL'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_attendance_invalid_id(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_attendance_invalid_choices(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"status": "invalid"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail',
                                    kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_put_attendance_invalid_choices(admin_factory, attendance_factory,
                                        authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "invalid"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_put_patch_attendance_non(user_factory, attendance_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    patch_response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_403_FORBIDDEN
    assert patch_response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_attendance_non_admin(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
