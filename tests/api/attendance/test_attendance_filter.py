import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status


def test_filter_attendance(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-list') + "?employee_id={}&date={}".format(employee.id, '2012-03-23'))
    assert response.status_code == status.HTTP_200_OK


def test_filter_attendance_invalid_format(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    client = authed_token_client_generator(user)
    with pytest.raises(ValueError) as e:
        client.get(reverse('attendance-list') + "?employee_id={}&date={}".format(employee.id, '2012-'))
    assert e.value.args[0] == 'Invalid date format'


def test_filter_attendance_invalid_employee_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    with pytest.raises(ValidationError) as e:
        client.get(reverse('attendance-list') + "?employee_id=invalid&date=2012-07-03")
    assert e.value.message == 'Invalid employee id'
