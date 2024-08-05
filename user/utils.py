from django.core.mail import EmailMessage


class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()


class UserRoles:
    USER = 'user'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    TEAM_LEAD = 'team_lead'

    CHOICES = (
        (USER, 'User'),
        (EMPLOYEE, 'Employee'),
        (ADMIN, 'Admin'),
        (TEAM_LEAD, 'team_lead'),
    )


def check_user_role(user):
    if user.is_admin:
        return UserRoles.ADMIN
    elif user.is_team_lead:
        return UserRoles.TEAM_LEAD
    elif user.is_employee:
        return UserRoles.EMPLOYEE
    else:
        return UserRoles.USER
