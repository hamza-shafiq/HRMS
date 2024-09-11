from hrms.permissions import BaseCustomPermission


class AnnouncementsPermission(BaseCustomPermission):
    pass

    def has_permission(self, request, view):
        if view.action == 'latest':
            if request.user.is_employee:
                return True
        return super().has_permission(request, view)
