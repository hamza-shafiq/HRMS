from django.urls import reverse
from rest_framework import status

from projects.models import Projects


def test_get_project_details(admin_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-detail', args=[project.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(project.id)
    assert response.json()['title'] == project.title


def test_get_project_details_non_admin(user_factory, project_factory, authed_token_client_generator):
    user = user_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-detail', args=[project.id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_update_project_details(admin_factory, project_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    project = project_factory()
    team_lead = employee_factory(national_id_number="123453")  # Hardcoded unique value
    account_manager = employee_factory(national_id_number="123452")  # Hardcoded unique value
    client = authed_token_client_generator(user)

    data = {
        "title": "Updated Project Title",
        "description": project.description,
        "tech_stack": project.tech_stack,
        "status": project.status,
        "added_by": project.added_by,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "team_lead": team_lead.id,
        "account_manager": account_manager.id,
    }

    response = client.put(reverse('projects-detail', args=[project.id]), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == data['title']

    # Updated assertion
    assert response.json()['team_lead']['team_lead_id'] == str(team_lead.id)


def test_update_project_details_non_admin(user_factory, project_factory, authed_token_client_generator):
    user = user_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    data = {"title": "Attempt to Update by Non-Admin"}
    response = client.put(reverse('projects-detail', args=[project.id]), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_project(admin_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('projects-detail', args=[project.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Projects.objects.filter(id=project.id).exists()


def test_delete_project_non_admin(user_factory, project_factory, authed_token_client_generator):
    user = user_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('projects-detail', args=[project.id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_invalid_project_details(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-detail', args=[999]))  # Assuming ID 999 does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_update_project_invalid_data(admin_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    data = {
        "title": "",
        "status": "invalid_status",
    }
    response = client.put(reverse('projects-detail', args=[project.id]), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.json()
    assert 'status' in response.json()
    assert response.json()['status'][0] == '"invalid_status" is not a valid choice.'
