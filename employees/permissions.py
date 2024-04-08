from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class DepartmentPermission(BaseCustomPermission):
    pass


class EmployeePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'employee_detail':
            if user_role == UserRoles.EMPLOYEE or (user_role == UserRoles.ADMIN and request.user.is_employee):
                return True
        return super().has_permission(request, view)


class EmployeeHistoryPermission(BaseCustomPermission):
    pass
