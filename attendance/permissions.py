from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class AttendancePermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'mark_attendance':
            if user_role == UserRoles.EMPLOYEE:
                return True
        return super().has_permission(request, view)
