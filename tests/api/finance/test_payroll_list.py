
from django.core import mail
from django.urls import reverse
from rest_framework import status

from finance.models import Payroll


def test_payroll_serializer_create(admin_factory, employee_factory,
                                   authed_token_client_generator, mailoutbox, celery_eager_run_on_commit):
    employee = employee_factory(email='employee@gmail.com')
    user = admin_factory()
    client = authed_token_client_generator(user)

    data = {
        'employee': str(employee.id),
        'basic_salary': 2000,
        'month': 'MAY',
        'year': '2023',
        'released': True
    }
    response = client.post(reverse('payroll-list'), data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Payroll.objects.filter(id=response.data['id']).exists()
    assert len(mail.outbox) == 1  # Assuming only one email is sent
    email = mail.outbox[0]
    assert email.subject == 'Payroll Generated'
    assert email.to == [employee.email]
