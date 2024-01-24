from rest_framework import permissions

from user.utils import UserRoles, check_user_role


class BaseCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if user_role == UserRoles.ADMIN:
            return True
        elif view.action == 'retrieve':
            if user_role == UserRoles.EMPLOYEE:
                return True
        elif view.action == 'list' or view.action == 'get':
            if user_role == UserRoles.Team_Lead:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        user_role = check_user_role(request.user)
        if user_role == UserRoles.ADMIN or obj.employee == request.user.employee:
            return True
        if user_role == UserRoles.Team_Lead or obj.employee == request.user.employee:
            return True
        return False
