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
            if UserRoles.ADMIN in user_role or UserRoles.TEAM_LEAD in user_role:
                return True
            return False
        if view.action == 'partial_update':
            if UserRoles.EMPLOYEE in user_role:
                return True
        if view.action == 'destroy':
            return True
        return super().has_permission(request, view)
