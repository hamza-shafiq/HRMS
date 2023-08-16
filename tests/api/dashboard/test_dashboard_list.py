from django.urls import reverse
from rest_framework import status


def test_get_statistics(admin_factory, employee_factory, asset_factory, recruit_factory,
                        authed_token_client_generator):
    employee = employee_factory()
    data = {"action": "check-in"}
    client_employee = authed_token_client_generator(employee)
    client_employee.post(reverse('attendance-mark-attendance'), data=data)
    asset_factory()
    recruit = recruit_factory()
    employee.employee_status = "FIRED"
    recruit.status = "PENDING"
    employee.save()
    recruit.save()
    employee.refresh_from_db()
    recruit.refresh_from_db()
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dashboard-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['total_departments'] == 1
    assert response.json()['total_employees'] == 1
    assert response.json()['present_employees'] == 0
    assert response.json()['total_assets'] == 1
    assert response.json()['total_assignee'] == 0
    assert response.json()['total_recruits'] == 1
    assert response.json()['pending_recruits'] == 1
    assert response.json()['total_attendees'] == 1


def test_get_statistics_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dashborad-employee_dashboard'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
