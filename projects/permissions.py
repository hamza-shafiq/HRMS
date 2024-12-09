from rest_framework.permissions import BasePermission
from employees.models import Employee
from hrms.permissions import BaseCustomPermission
from user.models import User


class ProjectPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_admin and user.is_employee:
            # Employees can only view projects (list and retrieve actions)
            if view.action in ['list', 'retrieve']:
                return True
            return False  # Employees cannot create, update, or delete projects

        elif user.is_admin:
            # Admin users can perform all actions
            return True

        elif user.is_employee:
            # Team leads can perform all actions (create, update, delete, etc.)
            try:
                employee = Employee.objects.get(id=user.id)
                if employee.is_team_lead:
                    return True  # Team leads have full access
            except Employee.DoesNotExist:
                pass

        return False  # If none of the above conditions match, deny permission
