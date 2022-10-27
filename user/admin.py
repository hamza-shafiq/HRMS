from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'is_staff')


admin.site.register(User, UserAdmin)
