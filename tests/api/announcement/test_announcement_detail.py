from django.urls import reverse
from rest_framework import status

from announcements.models import Announcements


def test_update_announcement(admin_factory, announcement_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    announcement = announcement_factory()
    data = {"title": "Updated Title"}
    response = client.patch(reverse('announcements-detail', kwargs={'pk': announcement.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert Announcements.objects.get(id=announcement.id).title == "Updated Title"


def test_update_announcement_non_admin(user_factory, announcement_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    announcement = announcement_factory()
    data = {"title": "Updated Title"}
    response = client.patch(reverse('announcements-detail', kwargs={'pk': announcement.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_announcement(admin_factory, announcement_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    announcement = announcement_factory()
    response = client.delete(reverse('announcements-detail', kwargs={'pk': announcement.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Announcements.deleted_objects.count() == 1
    assert Announcements.objects.count() == 0


def test_delete_announcement_non_admin(user_factory, announcement_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    announcement = announcement_factory()
    response = client.delete(reverse('announcements-detail', kwargs={'pk': announcement.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_announcement_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('announcements-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('announcements-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_update_announcement_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    data = {"title": "Updated Title"}
    response = client.patch(reverse('announcements-detail', kwargs={'pk': user.id}), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'
