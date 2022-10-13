from django.urls import reverse
from rest_framework import status
from assets.models import Asset


def test_get_assets_admin(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    assets = asset_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('asset-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['asset_model'] == assets.asset_model


def test_get_assets_employee(user_factory, asset_factory, authed_token_client_generator):
    user = user_factory()
    assets = asset_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('asset-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['asset_model'] == assets.asset_model


def test_create_asset(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"title": "Laptop", "asset_type": "Machine", "asset_model": "WO11", "cost": 5000}
    client = authed_token_client_generator(user)
    response = client.post(reverse('asset-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['asset_model'] == data['asset_model']


def test_create_asset_invalid_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine",
        "asset_model": "WO11",
        "cost": 'invalid.com'
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('asset-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_asset_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine"
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('asset-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_asset_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine",
        "asset_model": "WO11",
        "cost": 'invalid.com'
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('asset-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_asset_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('asset-list'))
    assert len(response.json()) == Asset.objects.all().count()
