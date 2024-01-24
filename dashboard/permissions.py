from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class DashboardPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        if view.action == 'employee_dashboard':
            if request.user.is_employee:
                return True
        return super().has_permission(request, view)
