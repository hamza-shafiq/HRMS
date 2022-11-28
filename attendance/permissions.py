from hrms.permissions import BaseCustomPermission
from user.utils import UserRoles, check_user_role


class AttendancePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'mark_attendance' or view.action == 'check_today_attendance':
            if user_role == UserRoles.EMPLOYEE:
                return True
        return super().has_permission(request, view)


class LeavesPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'create':
            if user_role == UserRoles.EMPLOYEE:
                return True
        return super().has_permission(request, view)
