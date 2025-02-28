from django.urls import reverse
from rest_framework import status

from projects.models import Assignment


def test_get_assignments(admin_factory, assignment_factory, authed_token_client_generator):
    user = admin_factory()
    assignment = assignment_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assignment-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['id'] == assignment.id


def test_create_assignment(admin_factory, employee_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory(national_id_number="123453")
    project = project_factory()
    data = {
        "employee": employee.id,
        "project": project.id,
        "start_date": "2022-07-01",
        "end_date": "2023-07-01",
        "engagement_type": "full_time",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('assignment-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['employee'] == str(employee.id)


def test_create_assignment_invalid_engagement_type(admin_factory, employee_factory,
                                                   project_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory(national_id_number="123453")
    project = project_factory()
    data = {
        "employee": employee.id,
        "project": project.id,
        "start_date": "2022-07-01",
        "end_date": "2023-07-01",
        "engagement_type": "intern",  # Invalid engagement type
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('assignment-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['engagement_type'][0] == '"intern" is not a valid choice.'


def test_get_assignments_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assignment-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_assignments_count(admin_factory, assignment_factory, authed_token_client_generator):
    user = admin_factory()
    assignment_factory.create_batch(5)  # Create multiple assignments
    client = authed_token_client_generator(user)
    response = client.get(reverse('assignment-list'))
    assert len(response.json()['results']) == Assignment.objects.all().count()
