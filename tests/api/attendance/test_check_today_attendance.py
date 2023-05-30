from django.urls import reverse
from rest_framework import status


def test_get_today_attendance(employee_factory, authed_token_client_generator):
    user = employee_factory()
    data = {"action": "check-in"}
    client = authed_token_client_generator(user)
    client.post(reverse('attendance-mark-attendance'), data=data)
    response = client.get(reverse('attendance-check-today-attendance'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['employee'] == str(user.id)


def test_get_today_attendance_no_data(employee_factory, authed_token_client_generator):
    user = employee_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('attendance-check-today-attendance'))
    assert response.status_code == status.HTTP_200_OK
    # assert response.json()['detail'] == 'You did not check-in today'
