# from user.utils import UserRoles, check_user_role
from employees.models import Employee
from hrms.permissions import BaseCustomPermission


class DashboardPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_admin and user.is_employee:
            employee = Employee.objects.get(id=user.id)
            if view.action == 'team_lead_dashboard':
                if employee.is_team_lead:
                    return True
            elif view.action == 'employee_dashboard':
                return True
        elif user.is_admin and user.is_employee:
            try:
                employee = Employee.objects.get(id=user.id)
                if view.action == 'team_lead_dashboard':
                    if employee.is_team_lead:
                        return True
            except Employee.DoesNotExist:
                pass
        return super().has_permission(request, view)
