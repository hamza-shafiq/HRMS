from django.urls import reverse
from rest_framework import status

from tasks.models import Tasks


def test_retrieve_task(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('tasks-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == Tasks.objects.count()


def test_create_task(admin_factory, employee_factory, authed_token_client_generator):
    admin = admin_factory()
    employee = employee_factory()
    employee2 = employee_factory()
    data = {
        "title": "My Title",
        "description": "My Detail",
        "deadline": "2024-02-01",
        "employee": employee.id,
        "assigned_by": employee2.id
    }
    client = authed_token_client_generator(admin)
    response = client.post(reverse('tasks-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == str(data['title'])
    assert response.json()['employee']['employee_id'] == str(data['employee'])
    assert response.json()['assigned_by']['assigned_by_id'] == str(data['assigned_by'])


def test_create_task_invalid_id(admin_factory, employee_factory, authed_token_client_generator):
    admin = admin_factory()
    employee = employee_factory()
    data = {
        "title": "My Title",
        "description": "My Detail",
        "deadline": "2024-02-01",
        "employee": "invalid_id",
        "assigned_by": employee.id
    }
    client = authed_token_client_generator(admin)
    response = client.post(reverse('tasks-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
