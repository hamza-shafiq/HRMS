from django.urls import reverse
from rest_framework import status


def test_filter_attendance(admin_factory, attendance_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list') + "?employee_id={}&date={}".format(employee.id, '2012-03-23'))
    assert response.status_code == status.HTTP_200_OK


def test_filter_attendance_invalid_format(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list') + "?employee_id={}&date={}".format(employee.id, '2012-'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == 'Invalid date format or employee id'


def test_filter_attendance_invalid_employee_id(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list') + "?employee_id={}&date={}".format("invalid", '2012-03-23'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == 'Invalid date format or employee id'
