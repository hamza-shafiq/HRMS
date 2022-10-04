from rest_framework_roles.roles import is_admin


def is_employee(request, view):
    return request.user.is_employee


ROLES = {
    'admin': is_admin,
    'employee': is_employee
}
