from django.core.mail import EmailMessage

from employees.models import Employee


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
    roles = []

    # Check if the user is an admin
    if user.is_admin:
        roles.append(UserRoles.ADMIN)

    # Check if the user is an employee
    if user.is_employee:
        roles.append(UserRoles.EMPLOYEE)

        # If the user is an employee, check if they are also a team lead
        try:
            employee = Employee.objects.get(id=user.id)
            if employee.is_team_lead:
                roles.append(UserRoles.TEAM_LEAD)
        except Employee.DoesNotExist:
            pass

    # If no roles were added (the user is neither admin nor employee), add USER
    if not roles:
        roles.append(UserRoles.USER)

    return roles
