from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class RecruitsPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        usr_role = check_user_role(request.user)
        if view.action == 'list':
            if usr_role == UserRoles.EMPLOYEE:
                return False
        return super().has_permission(request, view)
