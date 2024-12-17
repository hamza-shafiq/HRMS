from rest_framework.permissions import BasePermission
from employees.models import Employee
from hrms.permissions import BaseCustomPermission
from user.models import User


class ProjectPermission(BaseCustomPermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_admin and user.is_employee:

            if view.action in ['list', 'retrieve']:
                return True
            return True

        elif user.is_admin:
            return True

        elif user.is_employee:
            try:
                employee = Employee.objects.get(id=user.id)
                if employee.is_team_lead:
                    return True
            except Employee.DoesNotExist:
                pass
        return super().has_permission(request, view)


    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin:
            return True

        elif user.is_employee:
            try:
                employee = Employee.objects.get(id=user.id)
                if employee.is_team_lead:
                    return True
            except Employee.DoesNotExist:
                pass

        return False

