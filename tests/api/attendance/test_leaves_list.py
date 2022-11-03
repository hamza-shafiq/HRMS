from django.urls import reverse
from rest_framework import status

from attendance.models import Leaves


def test_get_leaves_admin(admin_factory, leaves_factory, authed_token_client_generator):
    user = admin_factory()
    leaves = leaves_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('leaves-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['leave_type'] == leaves.leave_type


def test_create_leave(admin_factory, employee_factory, authed_token_client_generator):
    user = admin_factory()
    employee = employee_factory()
    data = {"employee": employee.id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('leaves-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['leave_type'] == data['leave_type']


def test_create_leaves_employee(employee_factory, authed_token_client_generator):
    user = employee_factory()
    data = {"employee": user.id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('leaves-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['leave_type'] == data['leave_type']


def test_create_leave_invalid_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"employee": user.id, "leave_type": "casual", "reason": "urgent work",
            "request_date": "2022-07-02", "from_date": "2022-07", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('leaves-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_leave_incomplete_data(admin_factory, authed_token_client_generator):
    user = admin_factory()
    data = {"from_date": "2022-07-03", "to_date": "2022-07-04"}
    client = authed_token_client_generator(user)
    response = client.post(reverse('leaves-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['employee'][0] == 'This field is required.'


def test_get_leave_count(admin_factory, authed_token_client_generator):
    user = admin_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('leaves-list'))
    assert response.json()['count'] == Leaves.objects.all().count()


def test_get_leaves_non_admin(user_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('leaves-list'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'You do not have permission to perform this action.'
