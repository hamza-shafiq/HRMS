from django.urls import reverse
from rest_framework import status

from recruitments.models import RecruitsHistory


def test_update_employment_history(admin_factory, recruits_history_factory,
                                   authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    employee_history = recruits_history_factory()
    data = {"remarks": "Updated Remarks"}
    response = client.patch(reverse('recruits_history-detail', kwargs={'pk': employee_history.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert RecruitsHistory.objects.get(id=employee_history.id).remarks == "Updated Remarks"


def test_update_recruit_history_non_admin(user_factory, recruits_history_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    employee_history = recruits_history_factory()
    data = {"remarks": "Updated Remarks"}
    response = client.patch(reverse('recruits_history-detail', kwargs={'pk': employee_history.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_recruit_history(admin_factory, recruits_history_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    employee_history = recruits_history_factory()
    response = client.delete(reverse('recruits_history-detail', kwargs={'pk': employee_history.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert RecruitsHistory.deleted_objects.count() == 1
    assert RecruitsHistory.objects.count() == 0


def test_delete_employee_non_admin(user_factory, recruits_history_factory, authed_token_client_generator):
    user = user_factory()
    employee_history = recruits_history_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('recruits_history-detail', kwargs={'pk': employee_history.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_delete_recruit_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('recruits_history-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('recruits_history-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_update_recruit_history_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    data = {"remarks": "Updated Remarks"}
    response = client.patch(reverse('recruits_history-detail', kwargs={'pk': user.id}), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'
