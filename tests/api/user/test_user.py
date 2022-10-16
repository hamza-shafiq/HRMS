from django.urls import reverse
from rest_framework import status


def test_register_user(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze23", "password": "paklove"}
    response = rest_client.post(reverse('register'), data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


def test_login(user_factory, rest_client):
    user = user_factory(password="paklove")
    data = {"email": user.email, "password": "paklove"}
    response = rest_client.post(reverse('login'), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_logout(user_factory, rest_client):
    user = user_factory(password="paklove")
    data = {"email": user.email, "password": "paklove"}
    response = rest_client.post(reverse('login'), data=data, format='json')
    token = response.json()['tokens'].split("refresh': '")[1].split("', '")[0]
    response = rest_client.post(reverse('logout'), data={"refresh": token},  format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_register_user_email_verification(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze23", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    body = mailoutbox[0].body
    token = body.split('=')[1]
    data = {"token": token}
    response = rest_client.get(reverse('email-verify'), data)
    assert response.status_code == status.HTTP_200_OK


def test_register_user_invalid_password_length(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze", "password": "pak"}
    response = rest_client.post(reverse('register'), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_user_invalid_email_format(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "invalid", "username": "shahroze", "password": "paklove"}
    response = rest_client.post(reverse('register'), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_user_missing_data(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze"}
    response = rest_client.post(reverse('register'), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_email_verification_invalid_token(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze23", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    data = {"token": 'invalid'}
    response = rest_client.get(reverse('email-verify'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == 'Invalid token'


def test_request_passwrord_reset_user(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    response = rest_client.post(reverse('request-reset-email'), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_passwrord_reset_email_verification(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    rest_client.post(reverse('request-reset-email'), data=data, format='json')
    body = mailoutbox[1].body
    mail_data = body.split('reset/')[1]
    uidb64 = mail_data.split('/')[0]
    token = mail_data.split('/')[1]
    response = rest_client.get(reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token}))
    assert response.status_code == status.HTTP_200_OK


def test_set_new_password(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    rest_client.post(reverse('request-reset-email'), data=data, format='json')
    body = mailoutbox[1].body
    mail_data = body.split('reset/')[1]
    uidb64 = mail_data.split('/')[0]
    token = mail_data.split('/')[1]
    data = {"uidb64": uidb64, "token": token, "password": "paklove"}
    response = rest_client.patch(reverse('password-reset-complete'), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_request_passwrord_reset_no_email_data(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": ""}
    response = rest_client.post(reverse('request-reset-email'), data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_request_passwrord_reset_user_email_not_exist(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com"}
    response = rest_client.post(reverse('request-reset-email'), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_passwrord_reset_email_verification_wrong_token(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "gondal@gmail.com", "username": "shahroze", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    rest_client.post(reverse('request-reset-email'), data=data, format='json')
    body = mailoutbox[1].body
    mail_data = body.split('reset/')[1]
    uidb64 = mail_data.split('/')[0]
    response = rest_client.get(reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': 'invalid'}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_set_new_password_invalid_token(rest_client, celery_eager_run_on_commit, mailoutbox):
    data = {"email": "user@gmail.com", "username": "shahroze", "password": "paklove"}
    rest_client.post(reverse('register'), data=data, format='json')
    rest_client.post(reverse('request-reset-email'), data=data, format='json')
    body = mailoutbox[1].body
    mail_data = body.split('reset/')[1]
    uidb64 = mail_data.split('/')[0]
    data = {"uidb64": uidb64, "token": "invalid", "password": "paklove"}
    response = rest_client.patch(reverse('password-reset-complete'), data=data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_non_user(rest_client):
    data = {"email": "invalid@gmail.com", "password": "invalid"}
    response = rest_client.post(reverse('login'), data=data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_empty_token(rest_client):
    response = rest_client.post(reverse('logout'), data={"refresh": ""},  format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
