from django.urls import reverse
from rest_framework import status

from projects.models import Assignment


def test_get_assignment_detail(admin_factory, assignment_factory, authed_token_client_generator):
    user = admin_factory()
    assignment = assignment_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assignment-detail', kwargs={'pk': assignment.id}))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == assignment.id


def test_update_assignment(admin_factory, employee_factory, project_factory,
                           assignment_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory(national_id_number="123456")
    project = project_factory()
    assignment = assignment_factory()
    data = {
        "employee": employee.id,
        "project": project.id,
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "engagement_type": "part_time",
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('assignment-detail', kwargs={'pk': assignment.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['employee'] == str(employee.id)
    assert response.json()['project'] == str(project.id)
    assert response.json()['engagement_type'] == data['engagement_type']


def test_partial_update_assignment(admin_factory, employee_factory, project_factory,
                                   assignment_factory, authed_token_client_generator):
    user = admin_factory()
    assignment = assignment_factory()
    data = {
        "end_date": "2024-12-31",
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('assignment-detail', kwargs={'pk': assignment.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['end_date'] == data['end_date']


def test_delete_assignment(admin_factory, assignment_factory, authed_token_client_generator):
    user = admin_factory()
    assignment = assignment_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('assignment-detail', kwargs={'pk': assignment.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Assignment.objects.filter(id=assignment.id).exists()


def test_get_assignment_detail_non_admin(user_factory, authed_token_client_generator, assignment_factory):
    user = user_factory()
    assignment = assignment_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assignment-detail', kwargs={'pk': assignment.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_update_assignment_non_admin(user_factory, authed_token_client_generator, assignment_factory):
    user = user_factory()
    assignment = assignment_factory()
    data = {
        "end_date": "2024-12-31",
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('assignment-detail', kwargs={'pk': assignment.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_assignment_non_admin(user_factory, authed_token_client_generator, assignment_factory):
    user = user_factory()
    assignment = assignment_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('assignment-detail', kwargs={'pk': assignment.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
