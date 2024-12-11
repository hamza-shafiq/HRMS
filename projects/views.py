from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from hrms.pagination import CustomPageNumberPagination
from .permissions import ProjectPermission
from .serializers import ProjectsSerializer
import django_filters
from .models import Projects


class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_by_title')
    assignee = django_filters.CharFilter(method='filter_by_assignee')
    status = django_filters.CharFilter(method='filter_by_status')

    class Meta:
        model = Projects
        fields = ['title', 'assignee', 'status']

    def filter_by_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    def filter_by_assignee(self, queryset, name, value):

        return queryset.filter(assignee__username__icontains=value)

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=value)

    def filter_queryset(self, queryset):
        portal = self.request.query_params.get('portal')
        user = self.request.user
        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = queryset.filter(assignment__team_lead=user.id)
        return super().filter_queryset(queryset)



class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter
