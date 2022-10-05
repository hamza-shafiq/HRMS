from django.contrib import admin
import attendance.models

admin.site.register(attendance.models.Attendance)
admin.site.register(attendance.models.Leaves)