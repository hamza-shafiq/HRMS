from django.urls import reverse
from rest_framework import status

from announcements.models import Announcements


def test_retrieve_announcement(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('announcements-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == Announcements.objects.count()


def test_retrieve_latest_announcement(employee_factory, announcement_factory, authed_token_client_generator):
    user = employee_factory()
    client = authed_token_client_generator(user)
    announcement_factory()
    response = client.get(reverse('announcements-latest'))
    assert response.status_code == status.HTTP_200_OK
    latest_detail = response.get('latest_detail')
    assert latest_detail != ""


def test_create_announcement(admin_factory, employee_factory, authed_token_client_generator):
    admin = admin_factory()
    employee = employee_factory()
    data = {
        "title": "My Title",
        "detail": "My Detail",
        "date_from": "2024-02-01",
        "date_to": "2024-04-01",
        "added_by": employee.id
    }
    client = authed_token_client_generator(admin)
    response = client.post(reverse('announcements-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == str(data['title'])
    assert response.json()['added_by']['added_by_id'] == str(data['added_by'])
