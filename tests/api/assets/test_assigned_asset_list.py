from django.urls import reverse
from rest_framework import status

from assets.models import AssignedAsset


def test_get_assignee(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assigned-asset-list'))
    assert response.status_code == status.HTTP_200_OK


def test_create_assignee(admin_factory, asset_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    employee = employee_factory()
    data = {"asset": asset.id, "employee": employee.id}
    client = authed_token_client_generator(user)
    response = client.post(reverse('assigned-asset-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['asset'] == str(data['asset'])


def test_create_assignee_incomplete_data(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    data = {"asset": asset.id}
    client = authed_token_client_generator(user)
    response = client.post(reverse('assigned-asset-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_assignee_non_admin(user_factory, asset_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    asset = asset_factory()
    employee = employee_factory()
    data = {"asset": asset.id, "employee": employee.id}
    client = authed_token_client_generator(user)
    response = client.post(reverse('assigned-asset-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_assignee_invalid_data(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    data = {"asset": asset.id, "employee": user.id}
    client = authed_token_client_generator(user)
    response = client.post(reverse('assigned-asset-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_assignee_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('assigned-asset-list'))
    assert len(response.json()) == AssignedAsset.objects.all().count()
