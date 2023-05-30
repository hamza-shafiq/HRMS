import tempfile

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status

from recruitments.models import Recruits


def test_get_recruits(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruits = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['first_name'] == recruits.first_name


def temp_file():
    file = tempfile.NamedTemporaryFile(mode='w+b')
    file.write(b'test file')
    file.seek(0)
    return file


def test_create_recruit(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    file = temp_file()
    data = {"referrers": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": file}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    file.close()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['first_name'] == data['first_name']


def test_create_recruit_invalid_data(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"referrers": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "invalid", "resume": 'https://g.com'}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['status'][0] == '"invalid" is not a valid choice.'


def test_create_recruit_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": 4353}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['first_name'][0] == 'This field is required.'


def test_create_recruit_with_invalid_referrer(admin_factory, authed_token_client_generator):
    user = admin_factory()
    file = temp_file()
    data = {"referrers": "invalid", "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": file}
    client = authed_token_client_generator(user)
    with pytest.raises(ValidationError) as e:
        client.post(reverse('recruits-list'), data=data)
    file.close()
    assert e.value.message == 'Invalid referrer id'


def test_get_recruits_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_create_recruit_non_admin(user_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_get_recruit_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert response.json()['count'] == Recruits.objects.all().count()
