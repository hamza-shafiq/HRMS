from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class PayrollPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        if view.action == 'check_payroll':
            if request.user.is_employee:
                return True
        return super().has_permission(request, view)
