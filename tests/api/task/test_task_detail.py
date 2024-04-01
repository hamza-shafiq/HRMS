from django.urls import reverse
from rest_framework import status

from tasks.models import Tasks


def test_update_task(admin_factory, task_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    task = task_factory()
    data = {"title": "Updated Title"}
    response = client.patch(reverse('tasks-detail', kwargs={'pk': task.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert Tasks.objects.get(id=task.id).title == "Updated Title"


def test_update_task_non_admin(user_factory, task_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    task = task_factory()
    data = {"title": "Updated Title"}
    response = client.patch(reverse('tasks-detail', kwargs={'pk': task.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_update_task_status(employee_factory, task_factory, authed_token_client_generator):
    user = employee_factory()
    client = authed_token_client_generator(user)
    task = task_factory(employee=user)
    data = {"status": "IN_PROGRESS"}
    response = client.patch(reverse('tasks-update-status', kwargs={'pk': task.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert Tasks.objects.get(id=task.id).status == "IN_PROGRESS"


def test_delete_announcement(admin_factory, task_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    task = task_factory()
    response = client.delete(reverse('tasks-detail', kwargs={'pk': task.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tasks.deleted_objects.count() == 1
    assert Tasks.objects.count() == 0


def test_delete_task_non_admin(user_factory, task_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    task = task_factory()
    response = client.delete(reverse('tasks-detail', kwargs={'pk': task.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_task_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('tasks-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('tasks-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_update_task_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    data = {"title": "Updated Title"}
    response = client.patch(reverse('tasks-detail', kwargs={'pk': user.id}), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'
