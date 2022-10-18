from hrms.permissions import BaseCustomPermission
from user.utils import check_user_role, UserRoles


class AssetsPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        check_user_role(request.user)
        return super().has_permission(request, view)


class AssignedAssetPermission(BaseCustomPermission):

    def has_permission(self, request, view):
        user_role = check_user_role(request.user)
        if view.action == 'list':
            if user_role == UserRoles.EMPLOYEE:
                return False
        return super().has_permission(request, view)
