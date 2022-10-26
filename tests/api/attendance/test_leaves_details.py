from django.urls import reverse
from rest_framework import status

from attendance.models import Leaves


def test_retrieve_leave(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), format='json')
    assert response.status_code == status.HTTP_200_OK


def test_patch_leave(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    data = {"reason": "urgent work", "request_date": "2022-07-02", "from_date": "2022-07-03",
            "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['reason'] == data['reason']


def test_put_leave(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    data = {"employee": leave.employee_id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['reason'] == data['reason']


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
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_leave_invalid_id(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {
        "reason": 'sickness'
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_leave_invalid_id(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leave = leaves_factory()
    data = {"employee": leave.employee_id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('leaves-detail', kwargs={'pk': user.id}), data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_leave_non_admin(user_factory, leaves_factory, authed_token_client_generator):
    user = user_factory()
    leave = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('leaves-detail', kwargs={'pk': leave.id}), format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_leave_non_admin(user_factory, leaves_factory, authed_token_client_generator):
    user = user_factory()
    leave = leaves_factory()
    data = {"reason": "urgent work", "request_date": "2022-07-02", "from_date": "2022-07-03",
            "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.patch(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_put_leave_non_admin(user_factory, leaves_factory, authed_token_client_generator):
    user = user_factory()
    leave = leaves_factory()
    data = {"employee": leave.employee_id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.put(reverse('leaves-detail', kwargs={'pk': leave.id}), data=data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
