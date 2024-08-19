# from user.utils import UserRoles, check_user_role
from employees.models import Employee
from hrms.permissions import BaseCustomPermission


class DashboardPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_admin and user.is_employee:
            employee = Employee.objects.get(id=user.id)
            if view.action == 'employee_dashboard':
                if not employee.is_team_lead or (employee.is_team_lead and 'team_lead_dashboard' not in request.path):
                    return True
            if view.action == 'team_lead_dashboard':
                if employee.is_team_lead:
                    return True
        return super().has_permission(request, view)
