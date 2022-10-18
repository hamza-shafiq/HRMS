from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class DepartmentPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        check_user_role(request.user)
        return super().has_permission(request, view)


class EmployeePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action in ['list']:
            if user_role == UserRoles.EMPLOYEE:
                return False
        return super().has_permission(request, view)
