from django.urls import reverse
from rest_framework import status

from employees.models import Tenure



def test_update_tenure(admin_factory, tenure_factory,
                                   authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    tenure = tenure_factory()
    data = {"allocated_leaves": 14}
    response = client.patch(reverse('tenure-detail', kwargs={'pk': tenure.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert Tenure.objects.get(id=tenure.id).allocated_leaves == 14


def test_update_tenure_non_admin(user_factory, tenure_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    tenure = tenure_factory()
    data = {"allocated_leaves": 8}
    response = client.patch(reverse('tenure-detail', kwargs={'pk': tenure.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_tenure(admin_factory, tenure_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    tenure = tenure_factory()
    response = client.delete(reverse('tenure-detail', kwargs={'pk': tenure.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tenure.deleted_objects.count() == 1
    assert Tenure.objects.count() == 0



def test_delete_tenure_non_admin(user_factory, tenure_factory, authed_token_client_generator):
    user = user_factory()
    tenure = tenure_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('tenure-detail', kwargs={'pk': tenure.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_delete_employee_tenure_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('tenure-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('tenure-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_update_tenure_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    data = {"allocated_leaves": 14}
    response = client.patch(reverse('tenure-detail', kwargs={'pk': user.id}), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'

