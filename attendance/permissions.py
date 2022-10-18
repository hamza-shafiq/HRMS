from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class AttendancePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action in ['create', 'update', 'partial_update']:
            if user_role == UserRoles.EMPLOYEE or user_role == UserRoles.ADMIN:
                return True
        elif view.action == 'update':
            if user_role == UserRoles.USER:
                return False
        elif view.action == 'partial_update':
            if user_role == UserRoles.USER:
                return False
        return super().has_permission(request, view)


class LeavePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action in ['list']:
            if user_role == UserRoles.EMPLOYEE:
                return False
        if view.action in ['create']:
            if user_role == UserRoles.EMPLOYEE:
                return True
        return super().has_permission(request, view)
