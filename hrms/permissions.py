from rest_framework import permissions
from user.utils import check_user_role, UserRoles


class BaseCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'create':
            if not user_role == UserRoles.ADMIN:
                return False
        elif view.action == 'retrieve':
            if user_role == UserRoles.USER:
                return False
        elif view.action == 'list':
            if user_role == UserRoles.USER:
                return False
        elif view.action in ['update', 'partial_update', 'destroy']:
            if not user_role == UserRoles.ADMIN:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        """ nothing to do here, we already checked everything, so ignore """
        return True
