from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from projects.models import Projects, Assignment

# Custom filter for Project Status
class ProjectStatusFilter(SimpleListFilter):
    title = 'Project Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return Projects.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'team_lead', 'account_manager')
    list_filter = (ProjectStatusFilter,)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'get_project_title', 'start_date', 'end_date', 'engagement_type')
    list_filter = ('engagement_type', 'start_date', 'end_date')


    def get_project_title(self, obj):
        return obj.project.title
    get_project_title.short_description = 'Project Title'

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Projects, ProjectAdmin)

