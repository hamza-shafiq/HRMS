from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class AttendancePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        if view.action == 'mark_attendance' or view.action == 'check_today_attendance'\
                or view.action == 'get_attendance':
            if request.user.is_employee:
                return True

        return super().has_permission(request, view)


class LeavesPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'create' or view.action == 'get_leave':
            if request.user.is_employee:
                return True
        if view.action == 'approve':
            if user_role == UserRoles.ADMIN or user_role == UserRoles.Team_Lead:
                return True
            return False
        if view.action == 'partial_update':
            if user_role == UserRoles.EMPLOYEE:
                return True
        if view.action == 'destroy':
            return True
        return super().has_permission(request, view)
