from django.urls import reverse
from rest_framework import status

from employees.models import Tenure


def test_retrieve_tenure(admin_factory, employee_factory, tenure_factory,
                                   authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    tenure = tenure_factory(employee=employee1)
    client = authed_token_client_generator(user)
    response = client.get(reverse('tenure-list') + f"?employee_id={employee1.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == Tenure.objects.filter(employee=employee1).count()
    assert response.json()['results'][0]['employee']['employee_id'] == str(tenure.employee.id)



def test_create_tenure(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    employee2 = employee_factory()
    data = {
        "employee": employee1.id,
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "allocated_leaves": 10,
        "added_by": employee2.id
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('tenure-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['employee']['employee_id'] == str(data['employee'])
    assert response.json()['added_by']['added_by_id'] == str(data['added_by'])



def test_create_tenure_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('tenure-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'






def test_create_tenure_invalid_id(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee1 = employee_factory()
    employee2 = employee_factory()
    valid_data = {
        "employee": employee1.id,  # Pass a valid employee ID
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "allocated_leaves": 10,
        "added_by": employee2.id
    }

    invalid_data = {
        "employee": "invalid_id",  # Pass an invalid employee ID
        "interval_from": "2024-02-01",
        "interval_to": "2024-02-28",
        "allocated_leaves": 10,
        "added_by": employee2.id
    }
    client = authed_token_client_generator(user)
    # Test with valid data
    response_valid = client.post(reverse('tenure-list'), data=valid_data)
    assert response_valid.status_code == status.HTTP_201_CREATED

    # Test with invalid data
    response_invalid = client.post(reverse('tenure-list'), data=invalid_data)
    assert response_invalid.status_code == status.HTTP_400_BAD_REQUEST