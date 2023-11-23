from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

import attendance.models


class LeaveStatusFilter(SimpleListFilter):
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return attendance.models.Leaves.STATUS_CHOICE

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class LeavesAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'from_date', 'to_date', 'status', 'approved_by')
    list_filter = (LeaveStatusFilter,)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'check_in', 'check_out', 'status')
    list_filter = (LeaveStatusFilter,)


admin.site.register(attendance.models.Leaves, LeavesAdmin)
admin.site.register(attendance.models.Attendance, AttendanceAdmin)
