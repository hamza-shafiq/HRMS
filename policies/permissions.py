from hrms.permissions import BaseCustomPermission


class PolicyPermission(BaseCustomPermission):
    pass

    def has_permission(self, request, view):
        return True
