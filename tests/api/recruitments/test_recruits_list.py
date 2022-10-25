from django.urls import reverse
from rest_framework import status
from recruitments.models import Recruits


def test_get_recruits(admin_factory, recruit_factory, authed_token_client_generator):
    user = admin_factory()
    recruits = recruit_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['first_name'] == recruits.first_name


def test_create_recruit(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['first_name'] == data['first_name']


def test_create_recruit_invalid_data(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "invalid", "resume": 'https://g.com'}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_recruit_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": 4353}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_recruits_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_recruit_non_admin(user_factory, employee_factory, authed_token_client_generator):
    user = user_factory()
    employee = employee_factory()
    data = {"referrer": employee.id, "first_name": "usama", "last_name": "tayyab", "email": 'g@gmail.com',
            "phone_number": '242525', "position": "dev", "status": "IN_PROCESS", "resume": "https://g.com"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('recruits-list'), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_recruit_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits-list'))
    assert len(response.json()) == Recruits.objects.all().count()
