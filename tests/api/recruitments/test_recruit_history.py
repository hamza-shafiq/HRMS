from django.urls import reverse
from rest_framework import status

from recruitments.models import RecruitsHistory


def test_retrieve_recruit_history(admin_factory, recruit_factory, recruits_history_factory,
                                  authed_token_client_generator):
    user = admin_factory()
    employee1 = recruit_factory()
    employee_history = recruits_history_factory(recruit=employee1)
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits_history-list') + f"?recruit_id={employee1.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == RecruitsHistory.objects.filter(recruit=employee1).count()
    assert response.json()['results'][0]['recruit']['recruit_id'] == str(employee_history.recruit_id)


def test_create_recruit_history(admin_factory, recruit_factory, employee_factory,
                                authed_token_client_generator):
    admin = admin_factory()
    employee1 = recruit_factory()
    employee2 = employee_factory()
    employee3 = employee_factory()
    data = {
        "recruit": employee1.id,
        "process_stage": "New Stage",
        "remarks": "New Remarks",
        "event_date": "2024-02-01",
        "conduct_by": employee2.id,
        "added_by": employee3.id
    }
    client = authed_token_client_generator(admin)
    response = client.post(reverse('recruits_history-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['recruit']['recruit_id'] == str(data['recruit'])
    assert response.json()['conduct_by']['conduct_by_id'] == str(data['conduct_by'])
    assert response.json()['added_by']['added_by_id'] == str(data['added_by'])


def test_create_recruit_history_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('recruits_history-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


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


def test_create_recruit_history_invalid_id(admin_factory, recruit_factory, employee_factory,
                                           authed_token_client_generator):
    user = admin_factory()
    employee1 = recruit_factory()
    employee2 = employee_factory()
    employee3 = employee_factory()
    valid_data = {
        "recruit": employee1.id,
        "process_stage": "My Stage",
        "remarks": "New Remarks",
        "event_date": "2024-02-01",
        "conduct_by": employee2.id,
        "added_by": employee3.id
    }

    invalid_data = {
        "recruit": "invalid_id",
        "process_stage": "New Subject",
        "remarks": "New Remarks",
        "event_date": "2024-02-01",
        "conduct_by": employee2.id,
        "added_by": employee3.id
    }
    client = authed_token_client_generator(user)
    # Test with valid data
    response_valid = client.post(reverse('recruits_history-list'), data=valid_data)
    assert response_valid.status_code == status.HTTP_201_CREATED

    # Test with invalid data
    response_invalid = client.post(reverse('recruits_history-list'), data=invalid_data)
    assert response_invalid.status_code == status.HTTP_400_BAD_REQUEST
