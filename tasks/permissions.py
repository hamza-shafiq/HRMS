from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class TasksPermission(BaseCustomPermission):
    pass

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'list' or view.action == 'update_status':
            if UserRoles.EMPLOYEE in user_role:
                return True
        return super().has_permission(request, view)
