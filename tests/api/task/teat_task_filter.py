from django.urls import reverse
from rest_framework import status


def test_filter_task(admin_factory, task_factory, authed_token_client_generator):
    user = admin_factory()
    tasks = task_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('tasks-list') + "?status=" + str(tasks.status))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['status'] == str(tasks.status)
