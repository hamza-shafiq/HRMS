from django.contrib import admin

from .models import User, Tenant


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'is_staff', 'get_tenant_name')

    def get_tenant_name(self, obj):
        return obj.tenant.name if obj.tenant else None

    fieldsets = (
        ('User Info', {'fields': ('email', 'username', 'tenant')}),
        ('Permissions', {'fields': ('is_verified', 'is_employee', 'is_active', 'is_staff', 'is_admin')}),
    )
    get_tenant_name.short_description = 'Tenant'


admin.site.register(User, UserAdmin)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
