from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class PayrollPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'check_payroll':
            if user_role == UserRoles.EMPLOYEE:
                return True
        return super().has_permission(request, view)
