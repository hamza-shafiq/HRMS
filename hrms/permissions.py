from rest_framework import permissions
from user.utils import check_user_role, UserRoles


class BaseCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if user_role == UserRoles.ADMIN:
            return True
        elif view.action == 'retrieve':
            if user_role == UserRoles.EMPLOYEE:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """ nothing to do here, we already checked everything, so ignore """
        return True
