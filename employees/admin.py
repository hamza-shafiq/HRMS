from django.contrib import admin

import employees.models

# Register your models here.
admin.site.register(employees.models.Employee)
admin.site.register(employees.models.Department)
