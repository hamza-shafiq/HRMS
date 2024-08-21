from django.urls import reverse
from rest_framework import status

from attendance.models import Attendance


def test_retrieve_attendance(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(attendance.id)


def test_retrieve_attendance_non_admin_team_lead(employee_factory, attendance_factory, authed_token_client_generator):
    teamlead1 = employee_factory(is_team_lead=True)
    teamlead2 = employee_factory(is_team_lead=True)
    emp1 = employee_factory(team_lead=teamlead1)
    emp2 = employee_factory(team_lead=teamlead2)
    attendance_factory(employee=emp1)
    attendance_factory(employee=emp1)
    attendance_factory(employee=emp2)
    client = authed_token_client_generator(teamlead1)
    response = client.get(reverse('attendance-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 2
    client = authed_token_client_generator(teamlead2)
    response = client.get(reverse('attendance-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1


def test_retrieve_attendance_employee(attendance_factory, authed_token_client_generator):
    attendance = attendance_factory()
    client = authed_token_client_generator(attendance.employee)
    response = client.get(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(attendance.id)


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
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06 12:12:12+00:00",
            "check_out": "2022-07-05 12:12:12+00:00",
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
    attendance.refresh_from_db()
    assert attendance.is_deleted
    assert Attendance.global_objects.count() == 1
    assert Attendance.deleted_objects.count() == 1
    assert Attendance.objects.count() == 0


def test_retrieve_delete_attendance_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('attendance-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('attendance-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_patch_attendance_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "status": 'EARLY_ARRIVAL'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_put_attendance_invalid_id(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_patch_attendance_invalid_choices(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"status": "invalid"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('attendance-detail',
                                    kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['status'][0] == '"invalid" is not a valid choice.'


def test_put_attendance_invalid_choices(admin_factory, attendance_factory,
                                        authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "invalid"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['status'][0] == '"invalid" is not a valid choice.'


def test_put_patch_attendance_non_admin(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    data = {"employee": attendance.employee_id, "check_in": "2022-07-06", "check_out": "2022-07-05",
            "status": "EARLY_ARRIVAL"}
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    patch_response = client.patch(reverse('attendance-detail', kwargs={'pk': attendance.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_403_FORBIDDEN
    assert put_response.json()['detail'] == 'You do not have permission to perform this action.'
    assert patch_response.status_code == status.HTTP_403_FORBIDDEN
    assert patch_response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_attendance_non_admin(user_factory, attendance_factory, authed_token_client_generator):
    user = user_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('attendance-detail', kwargs={'pk': attendance.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
