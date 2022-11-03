from django.urls import reverse
from rest_framework import status


def test_mark_attendance_check_in(employee_factory, authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "check-in"}
    client = authed_token_client_generator(employee)
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['success'] == 'employee checked-in successfully!'


def test_mark_attendance_check_out(employee_factory, authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "check-in"}
    client = authed_token_client_generator(employee)
    client.post(reverse('attendance-mark-attendance'), data=data)
    data = {"action": "check-out"}
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['success'] == 'employee checked-out successfully!'


def test_mark_attendance_invalid_action(employee_factory, authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "invalid"}
    client = authed_token_client_generator(employee)
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json()['error'] == 'Please enter valid action (check-in/check-out)'


def test_check_in_attendance_already_checked_in(employee_factory, authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "check-in"}
    client = authed_token_client_generator(employee)
    client.post(reverse('attendance-mark-attendance'), data=data)
    data = {"action": "check-in"}
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_208_ALREADY_REPORTED
    assert response.json()['error'] == 'Employee already checked-in today!'


def test_check_out_attendance_not_checked_in(employee_factory, authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "check-out"}
    client = authed_token_client_generator(employee)
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json()['error'] == 'Employee did not check-in today!'


def test_mark_attendance_non_employee(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"action": "check-in"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('attendance-mark-attendance'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['error'] == 'Only employee can mark the attendance'
