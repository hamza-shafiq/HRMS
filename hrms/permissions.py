from rest_framework import permissions

from user.utils import UserRoles, check_user_role


class BaseCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user_roles = check_user_role(request.user)

        if UserRoles.ADMIN in user_roles:
            return True

        if view.action == 'retrieve':
            if UserRoles.EMPLOYEE in user_roles:
                return True

        if view.action in ['list', 'get']:
            if UserRoles.TEAM_LEAD in user_roles:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        user_role = check_user_role(request.user)
        if UserRoles.ADMIN in user_role or obj.employee == request.user.employee:
            return True
        if UserRoles.TEAM_LEAD in user_role or obj.employee == request.user.employee:
            return True
        return False
