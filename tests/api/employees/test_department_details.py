from django.urls import reverse
from rest_framework import status


def test_retrieve_department(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('department-detail', kwargs={'pk': department.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['department_name'] == department.department_name


def test_put_department(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {
        "department_name": "Backend",
        "description": "test_description"
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('department-detail', kwargs={'pk': department.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['department_name'] == data['department_name']


def test_patch_department(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    data = {
        "department_name": "Backend",
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('department-detail', kwargs={'pk': department.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['department_name'] == data['department_name']


def test_delete_department(admin_factory, department_factory, authed_token_client_generator):
    user = admin_factory()
    department = department_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('department-detail', kwargs={'pk': department.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_put_department_non_admin(user_factory, department_factory, authed_token_client_generator):
    user = user_factory()
    department = department_factory()
    data = {
        "department_name": "Backend",
        "description": "test_description"
    }
    client = authed_token_client_generator(user)
    response = client.put(reverse('department-detail', kwargs={'pk': department.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_department_non_admin(user_factory, department_factory, authed_token_client_generator):
    user = user_factory()
    department = department_factory()
    data = {
        "department_name": "Backend",
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('department-detail', kwargs={'pk': department.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_department_non_admin(user_factory, department_factory, authed_token_client_generator):
    user = user_factory()
    department = department_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('department-detail', kwargs={'pk': department.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_delete_department_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    retrieve_response = client.get(reverse('department-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('department-detail', kwargs={'pk': user.id}), format='json')
    assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_put_patch_department_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "department_name": "Backend",
        "description": "test_description"
    }
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('department-detail', kwargs={'pk': user.id}), data=data, format='json')
    patch_response = client.patch(reverse('department-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
