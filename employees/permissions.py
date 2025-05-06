from hrms.permissions import BaseCustomPermission


class DepartmentPermission(BaseCustomPermission):
    pass


class EmployeePermission(BaseCustomPermission):

    def has_permission(self, request, view):

        if view.action in ['employee_detail', 'partial_update']:
            if request.user.is_employee:
                return True
        if request.user.is_admin:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if request.user.is_employee and obj == request.user.employee:
            return True
        return False


class EmployeeHistoryPermission(BaseCustomPermission):
    pass


class TenurePermission(BaseCustomPermission):
    pass
