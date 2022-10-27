from django.urls import reverse
from rest_framework import status

from assets.models import Asset


def test_retrieve_asset(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('asset-detail', kwargs={'pk': asset.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == asset.title


def test_put_asset(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine",
        "asset_model": "VV11",
        "cost": 5000
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('asset-detail', kwargs={'pk': asset.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == data['title']


def test_patch_asset(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    data = {
        "title": "Mobile",
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('asset-detail', kwargs={'pk': asset.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == data['title']


def test_delete_asset(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('asset-detail', kwargs={'pk': asset.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    asset.refresh_from_db()
    assert asset.is_deleted
    assert Asset.global_objects.count() == 1
    assert Asset.deleted_objects.count() == 1
    assert Asset.objects.count() == 0


def test_put_asset_non_admin(user_factory, asset_factory, authed_token_client_generator):
    user = user_factory()
    asset = asset_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine",
        "asset_model": "ZZ22",
        "cost": 5000
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('asset-detail', kwargs={'pk': asset.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_asset_non_admin(user_factory, asset_factory, authed_token_client_generator):
    user = user_factory()
    asset = asset_factory()
    data = {
        "title": "Backend",
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('asset-detail', kwargs={'pk': asset.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_asset_non_admin(user_factory, asset_factory, authed_token_client_generator):
    user = user_factory()
    asset = asset_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('asset-detail', kwargs={'pk': asset.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_delete_asset_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    retrieve_response = client.get(reverse('asset-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('asset-detail', kwargs={'pk': user.id}), format='json')
    assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_put_patch_asset_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "title": "Laptop",
        "asset_type": "Machine",
        "asset_model": "ZZ22",
        "cost": 5000
    }
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('asset-detail', kwargs={'pk': user.id}), data=data, format='json')
    patch_response = client.patch(reverse('asset-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
