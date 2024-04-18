from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'is_staff')

    def save_model(self, request, obj, form, change):
        field = 'password'
        super().save_model(request, obj, form, change)
        if change and field in form.changed_data and form.cleaned_data.get(field):
            obj.set_password(obj.password)
            obj.save()


admin.site.register(User, UserAdmin)
