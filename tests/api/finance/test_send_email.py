from django.db.models import signals
from django.urls import reverse
from factory.django import mute_signals
from rest_framework import status
from django.core import mail
from finance.models import Payroll


def test_send_mail_release_payroll(admin_factory, employee_factory, payroll_factory,
                                   authed_token_client_generator, mailoutbox, celery_eager_run_on_commit):
    with mute_signals(signals.post_save):
        employee = employee_factory(email='employee@gmail.com')
        admin_user = admin_factory()
        payroll = payroll_factory(employee=employee)
    client = authed_token_client_generator(admin_user)
    data = {
        'id': payroll.id,
        'employee': str(employee.id),
        'basic_salary': 2000,
        'month': 'JUNE',
        'year': '2023',
    }

    response = client.post(reverse('payroll-send-mail'), data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mailoutbox) == 1  # Assuming only one email is sent
    email = mailoutbox[0]
    assert email.subject == 'Payroll Generated'
    assert email.to == [employee.email]


def test_send_mail_salary_being_processed(admin_factory, employee_factory, payroll_factory,
                                          authed_token_client_generator, mailoutbox, celery_eager_run_on_commit):
    with mute_signals(signals.post_save):
        employee = employee_factory(email='employee@gmail.com')
        admin_user = admin_factory()
        payroll = payroll_factory(employee=employee)
    client = authed_token_client_generator(admin_user)
    data = {
        'id': payroll.id,
        'employee': str(employee.id),
        'basic_salary': 2000,
        'month': 'JUNE',
        'year': '2023',
        'released': True,
    }
    response = client.post(reverse('payroll-send-mail'), data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(mailoutbox) == 0
    unchanged_payroll = Payroll.objects.get(id=payroll.id)
    assert unchanged_payroll.released == False
