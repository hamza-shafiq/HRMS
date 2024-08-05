from hrms.permissions import BaseCustomPermission

# from user.utils import UserRoles, check_user_role


class DashboardPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        # user_role = check_user_role(request.user)
        if view.action == 'employee_dashboard':
            if request.user.is_employee:
                return True
        if view.action == 'team_lead_dashboard':
            if request.user.is_team_lead:
                return True
        return super().has_permission(request, view)
