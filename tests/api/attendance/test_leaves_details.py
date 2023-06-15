import datetime

from django.urls import reverse
from rest_framework import status

from attendance.models import Leaves


def test_retrieve_leave(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('leaves-detail', kwargs={'pk': leave.id}), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(leave.id)


def test_patch_leave(employee_factory, leaves_factory, authed_token_client_generator):
    user = employee_factory()
    leave = leaves_factory(employee=user)
    data = {"reason": "urgent work", "request_date": "2022-07-02", "from_date": "2022-07-03",
            "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['reason'] == data['reason']


def test_patch_leave_after_approved_or_rejected(employee_factory, leaves_factory, authed_token_client_generator):
    user = employee_factory()
    leave = leaves_factory(employee=user, status="APPROVED")
    data = {"request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == 'Cannot update Leave Information after APPROVED status'


def test_delete_leave(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('leaves-detail', kwargs={'pk': leave.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    leave.refresh_from_db()
    assert leave.is_deleted
    assert Leaves.global_objects.count() == 1
    assert Leaves.deleted_objects.count() == 1
    assert Leaves.objects.count() == 0


def test_retrieve_delete_leave_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    get_response = client.delete(reverse('leaves-detail', kwargs={'pk': user.id}), format='json')
    delete_response = client.delete(reverse('leaves-detail', kwargs={'pk': user.id}), format='json')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'Not found.'
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.json()['detail'] == 'Not found.'


def test_patch_leave_invalid_id(employee_factory, authed_token_client_generator):
    user = employee_factory(is_staff=True, is_admin=True)
    data = {
        "reason": 'sickness'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_put_leave_invalid_id(employee_factory, leaves_factory, authed_token_client_generator):
    user = employee_factory(is_staff=True, is_admin=True)
    leave = leaves_factory()
    data = {"employee": leave.employee_id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('leaves-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found.'


def test_delete_leave_non_admin(employee_factory, leaves_factory, authed_token_client_generator):
    user = employee_factory(is_staff=True, is_admin=True)
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('leaves-detail', kwargs={'pk': leave.id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    leave.refresh_from_db()
    assert leave.is_deleted


def test_patch_leave_non_admin(employee_factory, leaves_factory, authed_token_client_generator):
    user = employee_factory()
    leave = leaves_factory()
    data = {"reason": "urgent work", "request_date": "2022-07-02", "from_date": "2022-07-03",
            "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_put_leave_non_admin(user_factory, leaves_factory, authed_token_client_generator):
    user = user_factory()
    leave = leaves_factory()
    data = {"employee": leave.employee_id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_update_leave_status(leaves_factory, employee_factory, authed_token_client_generator):
    data = {
        "status": "APPROVED"
    }
    approved_by = employee_factory(is_staff=True, is_admin=True)
    employee = employee_factory()
    leave = leaves_factory(employee=employee, from_date=datetime.datetime.now(),
                           to_date=datetime.datetime.now() + datetime.timedelta(days=2))
    client = authed_token_client_generator(approved_by)
    response = client.patch(reverse('leaves-approve', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result['employee'] == str(employee.id)
    assert result['number_of_days'] == '3'
    assert result['remaining_leaves'] == '17'
    assert result['status'] == "APPROVED"
    assert response.json()['approved_by']['approved_by_name'] == approved_by.get_full_name
