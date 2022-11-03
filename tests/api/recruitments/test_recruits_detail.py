from django.urls import reverse
from rest_framework import status

from recruitments.models import Recruits


def test_retrieve_recruit(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruit = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-detail', kwargs={'pk': recruit.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(recruit.id)


def test_put_recruit(admin_factory, recruit_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    recruit = recruit_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "Sajid", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['first_name'] == data['first_name']


def test_patch_recruit(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruit = recruit_factory()
    data = {"first_name": "Sajid", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525'}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['first_name'] == data['first_name']


def test_delete_recruit(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruit = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('recruits-detail', kwargs={'pk': recruit.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    recruit.refresh_from_db()
    assert recruit.is_deleted
    assert Recruits.global_objects.count() == 1
    assert Recruits.deleted_objects.count() == 1
    assert Recruits.objects.count() == 0


def test_put_patch_recruit_invalid_status(admin_factory, employee_factory, recruit_factory,
                                          authed_token_client_generator):
    user = admin_factory()
    recruit = recruit_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "Sajid", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "invalid", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    patch_response = client.patch(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_400_BAD_REQUEST
    assert put_response.json()['status'][0] == '"invalid" is not a valid choice.'
    assert patch_response.status_code == status.HTTP_400_BAD_REQUEST
    assert patch_response.json()['status'][0] == '"invalid" is not a valid choice.'


def test_put_patch_recruit_non_admin(user_factory, recruit_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    recruit = recruit_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "Sajid", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    patch_response = client.patch(reverse('recruits-detail', kwargs={'pk': recruit.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_403_FORBIDDEN
    assert put_response.json()['detail'] == 'You do not have permission to perform this action.'
    assert patch_response.status_code == status.HTTP_403_FORBIDDEN
    assert patch_response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_recruit_non_admin(user_factory, recruit_factory, authed_token_client_generator):
    user = user_factory()
    recruit = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('recruits-detail', kwargs={'pk': recruit.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_delete_recruit_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    retrieve_response = client.get(reverse('recruits-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('recruits-detail', kwargs={'pk': user.id}), format='json')
    assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND
    assert retrieve_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_put_patch_recruit_invalid_id(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "Sajid", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    put_response = client.put(reverse('recruits-detail', kwargs={'pk': user.id}), data=data, format='json')
    patch_response = client.patch(reverse('recruits-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert put_response.status_code == status.HTTP_404_NOT_FOUND
    assert put_response.json()['detail'] == 'Not found.'
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'Not found.'
