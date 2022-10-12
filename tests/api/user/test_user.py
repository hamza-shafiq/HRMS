from django.urls import reverse
from rest_framework import status


def test_register_user(rest_client):
    data = {
     "email": "gondal@gmail.com",
     "username": "shahroze23",
     "password": "paklove"
    }
    response = rest_client.post(reverse('register'), data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(rest_client):
    data = {
     "email": "gondal@gmail.com",
     "password": "paklove"
    }
    response = rest_client().post(reverse('login'), data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

