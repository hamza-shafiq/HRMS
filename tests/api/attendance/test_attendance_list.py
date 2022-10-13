from django.urls import reverse
from rest_framework import status
from attendance.models import Attendance


def test_get_attendances(admin_factory, attendance_factory, authed_token_client_generator):
    user = admin_factory()
    attendance = attendance_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == str(attendance.id)


def test_create_attendance(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"employee": employee.id, "check_in": "2022-07-06", "check_out": "2022-07-06", "status": "ON_TIME"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('attendance-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_attendances_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"check_in": "2022-07-06", "check_out": "2022-07-06", "status": "ON_TIME"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('attendance-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_attendances_invalid_status(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"employee": employee.id, "check_in": "2022-07-06", "check_out": "2022-07-06", "status": "invalid"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('attendance-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_attendances_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list'))
    assert len(response.json()) == Attendance.objects.all().count()
