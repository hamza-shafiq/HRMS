from datetime import datetime

from django.urls import reverse
from rest_framework import status


def test_filter_attendance(admin_factory, attendance_factory, employee_factory, authed_token_client_generator):
    data = {"action": "check-in"}
    attendance = attendance_factory()
    client = authed_token_client_generator(attendance.employee)
    client.post(reverse('attendance-mark-attendance'), data=data)
    user = admin_factory()
    date = datetime.now().date()
    client = authed_token_client_generator(user)
    # response = client.get(reverse('attendance-list')
    # + "?employee_id={}&date={}".format(attendance.employee.id, date))
    response = client.get(reverse('attendance-list') + "?date={}".format(date))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['employee'] == str(attendance.employee.id)


def test_filter_attendance_invalid_format(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    # employee = employee_factory()
    client = authed_token_client_generator(user)
    # response = client.get(reverse('attendance-list') + "?employee_id={}&date={}".format(employee.id, '2012-'))
    response = client.get(reverse('attendance-list') + "?date={}".format('2012-'))
    assert response.json()['error'] == 'Invalid date format'

# def test_filter_attendance_invalid_employee_id(admin_factory, authed_token_client_generator):
#     user = admin_factory()
#     client = authed_token_client_generator(user)
#     response = client.get(reverse('attendance-list') + "?date=2012-07-03")
#     assert response.json()['detail'] == 'Invalid employee id'
