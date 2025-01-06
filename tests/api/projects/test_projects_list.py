from django.urls import reverse
from rest_framework import status

from projects.models import Projects


def test_get_projects(admin_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    project = project_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['id'] == str(project.id)


# def test_create_project(admin_factory, employee_factory, authed_token_client_generator):
#     user = admin_factory()
#     team_lead = employee_factory()
#     account_manager = employee_factory()
#
#     data = {
#         "title": "New Project",
#         "description": "A test project.",
#         "tech_stack": "Python, Django, React",
#         "status": "in_progress",
#         "added_by": "Test Admin",
#         "start_date": "2022-07-01",
#         "end_date": "2023-07-01",
#         "team_lead": team_lead.id,
#         "account_manager": account_manager.id,
#     }
#     client = authed_token_client_generator(user)
#     response = client.post(reverse('projects-list'), data=data)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json()['title'] == data['title']


def test_create_project_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "title": "",
        "description": "A test project without title.",
        "tech_stack": "Python",
        "status": "not_started",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('projects-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['title'][0] == 'This field may not be blank.'


def test_create_project_invalid_status(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    team_lead = employee_factory()
    account_manager = employee_factory()
    data = {
        "title": "Invalid Status Project",
        "description": "Project with invalid status.",
        "tech_stack": "Python, Django",
        "status": "unknown_status",
        "added_by": "Test Admin",
        "start_date": "2022-07-01",
        "end_date": "2023-07-01",
        "team_lead": team_lead.id,
        "account_manager": account_manager.id,
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('projects-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['status'][0] == '"unknown_status" is not a valid choice.'


def test_create_project_non_admin(user_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    team_lead = employee_factory()
    account_manager = employee_factory()
    data = {
        "title": "Non-Admin Project",
        "description": "A project by a non-admin user.",
        "tech_stack": "JavaScript",
        "status": "in_progress",
        "added_by": "Non-Admin User",
        "start_date": "2022-07-01",
        "end_date": "2023-07-01",
        "team_lead": team_lead.id,
        "account_manager": account_manager.id,
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('projects-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_projects_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_projects_count(admin_factory, project_factory, authed_token_client_generator):
    user = admin_factory()
    project_factory.create_batch(5)  # Create multiple projects
    client = authed_token_client_generator(user)
    response = client.get(reverse('projects-list'))
    assert len(response.json()['results']) == Projects.objects.all().count()
