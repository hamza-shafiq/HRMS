from hrms.permissions import BaseCustomPermission


class DepartmentPermission(BaseCustomPermission):
    pass


class EmployeePermission(BaseCustomPermission):

    def has_permission(self, request, view):

        if view.action == 'employee_detail':
            if request.user.is_employee:
                return True
        if request.user.is_admin:
            return True
        return super().has_permission(request, view)


class EmployeeHistoryPermission(BaseCustomPermission):
    pass
