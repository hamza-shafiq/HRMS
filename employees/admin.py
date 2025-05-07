from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

import employees.models


class EmployeeStatusFilter(SimpleListFilter):
    title = _('Employee Status')
    parameter_name = 'employee_status'

    def lookups(self, request, model_admin):
        return employees.models.Employee.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(employee_status=self.value())
        return queryset


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'employee_status', 'remaining_leaves')
    list_filter = (EmployeeStatusFilter,)
    search_fields = ['first_name', 'last_name']


class TenureAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'status', 'interval_from', 'interval_to', 'allocated_leaves',]


# Register your models here.
admin.site.register(employees.models.Employee, EmployeesAdmin)
admin.site.register(employees.models.Department)
admin.site.register(employees.models.EmployeeHistory)
admin.site.register(employees.models.Tenure, TenureAdmin)
