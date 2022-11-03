from django.urls import reverse
from rest_framework import status

from assets.models import AssignedAsset


def test_retrieve_assignee(admin_factory, assignee_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    client = authed_token_client_generator(user)
    response = client.patch(reverse('assigned-asset-detail', kwargs={'pk': assignee.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(assignee.id)


def test_patch_assignee(admin_factory, assignee_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    asset = asset_factory()
    data = {"asset": asset.id}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('assigned-asset-detail', kwargs={'pk': assignee.id}), data=data, format='json')
    assert response.json()['asset'] == str(data['asset'])


def test_put_assignee(admin_factory, assignee_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    asset = asset_factory()
    data = {"asset": asset.id, "employee": assignee.employee_id}
    client = authed_token_client_generator(user)
    response = client.put(reverse('assigned-asset-detail', kwargs={'pk': assignee.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['asset'] == str(data['asset'])


def test_delete_assignee(admin_factory, assignee_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('assigned-asset-detail', kwargs={'pk': assignee.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assignee.refresh_from_db()
    assert assignee.is_deleted
    assert AssignedAsset.global_objects.count() == 1
    assert AssignedAsset.deleted_objects.count() == 1
    assert AssignedAsset.objects.count() == 0


def test_retrieve_delete_assignee_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('assigned-asset-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('assigned-asset-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_patch_assignee_invalid_id(admin_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    asset = asset_factory()
    data = {"asset": asset.id}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('assigned-asset-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_put_assignee_invalid_id(admin_factory, assignee_factory, asset_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    asset = asset_factory()
    data = {"asset": asset.id, "employee": assignee.employee_id}
    client = authed_token_client_generator(user)
    response = client.put(reverse('assigned-asset-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_put_patch_assignee_invalid_data(admin_factory, assignee_factory, authed_token_client_generator):
    user = admin_factory()
    assignee = assignee_factory()
    data = {"asset": user.id, "employee": user.id}
    client = authed_token_client_generator(user)
    put_response = client.patch(reverse('assigned-asset-detail',
                                        kwargs={'pk': assignee.id}), data=data, format='json')
    patch_response = client.patch(reverse('assigned-asset-detail',
                                          kwargs={'pk': assignee.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_400_BAD_REQUEST
    assert patch_response.status_code == status.HTTP_400_BAD_REQUEST


def test_put_patch_assignee_non_admin(user_factory, assignee_factory, asset_factory, authed_token_client_generator):
    user = user_factory()
    assignee = assignee_factory()
    asset = asset_factory()
    data = {
        "asset": asset.id,
        "employee": assignee.employee_id
    }
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('assigned-asset-detail',
                                      kwargs={'pk': assignee.id}), data=data, format='json')
    patch_response = client.patch(reverse('assigned-asset-detail',
                                          kwargs={'pk': assignee.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_403_FORBIDDEN
    assert put_response.json()['detail'] == 'You do not have permission to perform this action.'
    assert patch_response.status_code == status.HTTP_403_FORBIDDEN
    assert put_response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_assignee_non_admin(user_factory, assignee_factory, authed_token_client_generator):
    user = user_factory()
    assignee = assignee_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('assigned-asset-detail', kwargs={'pk': assignee.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
