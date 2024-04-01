from django.urls import reverse
from rest_framework import status

from employees.models import EmployeeHistory


def test_retrieve_employee_history(admin_factory, employee_factory, employee_history_factory,
                                   authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    employee_history = employee_history_factory(employee=employee1)
    client = authed_token_client_generator(user)
    response = client.get(reverse('employee_history-list') + f"?employee_id={employee1.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == EmployeeHistory.objects.filter(employee=employee1).count()
    assert response.json()['results'][0]['employee']['employee_id'] == str(employee_history.employee_id)


def test_create_employee_history(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    employee2 = employee_factory()
    employee3 = employee_factory()
    data = {
        "employee": employee1.id,
        "subject": "New Subject",
        "remarks": "New Remarks",
        "increment": 200.00,
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "review_by": employee2.id,
        "review_date": "2024-03-01",
        "added_by": employee3.id
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('employee_history-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['employee']['employee_id'] == str(data['employee'])
    assert response.json()['review_by']['review_by_id'] == str(data['review_by'])
    assert response.json()['added_by']['added_by_id'] == str(data['added_by'])


def test_create_employee_history_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('employee_history-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_update_employment_history(admin_factory, employee_history_factory,
                                   authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    employee_history = employee_history_factory()
    data = {"subject": "Updated Subject"}
    response = client.patch(reverse('employee_history-detail', kwargs={'pk': employee_history.id}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert EmployeeHistory.objects.get(id=employee_history.id).subject == "Updated Subject"


def test_update_employment_history_non_admin(user_factory, employee_history_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    employee_history = employee_history_factory()
    data = {"subject": "Updated Subject"}
    response = client.patch(reverse('employee_history-detail', kwargs={'pk': employee_history.id}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_delete_employee_history(admin_factory, employee_history_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    employee_history = employee_history_factory()
    response = client.delete(reverse('employee_history-detail', kwargs={'pk': employee_history.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert EmployeeHistory.deleted_objects.count() == 1
    assert EmployeeHistory.objects.count() == 0


def test_delete_employee_non_admin(user_factory, employee_history_factory, authed_token_client_generator):
    user = user_factory()
    employee_history = employee_history_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('employee_history-detail', kwargs={'pk': employee_history.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_retrieve_delete_employee_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('employee_history-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('employee_history-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_update_employment_history_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    data = {"subject": "Updated Subject"}
    response = client.patch(reverse('employee_history-detail', kwargs={'pk': user.id}), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_create_employee_history_invalid_id(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    employee2 = employee_factory()
    employee3 = employee_factory()
    valid_data = {
        "employee": employee1.id,  # Pass a valid employee ID
        "subject": "New Subject",
        "remarks": "New Remarks",
        "increment": 200.00,
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "review_by": employee2.id,
        "review_date": "2024-03-01",
        "added_by": employee3.id
    }

    invalid_data = {
        "employee": "invalid_id",  # Pass an invalid employee ID
        "subject": "New Subject",
        "remarks": "New Remarks",
        "increment": 200.00,
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "review_by": employee2.id,
        "review_date": "2024-03-01",
        "added_by": employee3.id
    }
    client = authed_token_client_generator(user)
    # Test with valid data
    response_valid = client.post(reverse('employee_history-list'), data=valid_data)
    assert response_valid.status_code == status.HTTP_201_CREATED

    # Test with invalid data
    response_invalid = client.post(reverse('employee_history-list'), data=invalid_data)
    assert response_invalid.status_code == status.HTTP_400_BAD_REQUEST
