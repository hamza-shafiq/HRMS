from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from employees.serializers import EmployeeSerializer
from hrms.pagination import CustomPageNumberPagination
from .permissions import ProjectPermission
from .serializers import ProjectsSerializer, AssignmentSerializer
import django_filters
from .models import Projects, Assignment


class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_by_title')
    assignee = django_filters.CharFilter(method='filter_by_assignee')
    status = django_filters.CharFilter(method='filter_by_status')

    class Meta:
        model = Projects
        fields = ['title', 'assignee', 'status']

    def filter_by_title(self, queryset, name, value):
        return queryset.filter(title__icontains=value)


    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=value)

    def filter_queryset(self, queryset):
        portal = self.request.query_params.get('portal')
        user = self.request.user
        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = queryset.filter(team_lead_id=user.id)
        return super().filter_queryset(queryset)



class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter



    @action(detail=False, url_path="account_managers", methods=['get'])
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin :
            employees = Employee.objects.filter(department__department_name="Accounts")
        else:
            try:
                employee = Employee.objects.get(id=user.id)
                if employee.is_team_lead:
                    employees = Employee.objects.filter(department__department_name="Accounts")
                else:
                    return JsonResponse({'error': 'Permission denied'}, status=403)
            except Employee.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        return JsonResponse({'account_managers': serializer.data})






class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]
    pagination_class = CustomPageNumberPagination

    @action(detail=False, methods=['get'], url_path='employee_assignments')
    def get_employee_assignments(self, request):
        title=request.GET.get('title')
        status=request.GET.get('status')
        user = request.user

        try:
            assignments = Assignment.objects.filter(employee_id=user.id).select_related('project', 'employee')
            if title:
                assignments=assignments.filter(project__title=title )
            if status:
                assignments=assignments.filter(project__status=status)


            data = []
            for assignment in assignments:
                project_data = {
                    'project_id': assignment.project.id,
                    'project_title': assignment.project.title,
                    'project_description': assignment.project.description,
                    'project_status': assignment.project.status,
                    'assignment_id': assignment.id,
                    'start_date': assignment.start_date,
                    'end_date': assignment.end_date,
                    'engagement_type': assignment.engagement_type,
                    'project_teamlead': assignment.project.team_lead.get_full_name if assignment.project.team_lead else None,
                }
                data.append(project_data)

            return JsonResponse({
                'employee_id': user.id,
                'assignments': data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    @action(detail=False, methods=['get'], url_path='teamlead_assignments')
    def get_teamlead_assignments(self, request):
        user = request.user

        try:
            assignments = Assignment.objects.filter(employee_id=user.id).select_related('project', 'employee')

            data = []
            for assignment in assignments:
                project_data = {
                    'project_id': assignment.project.id,
                    'project_title': assignment.project.title,
                    'project_description': assignment.project.description,
                    'project_status': assignment.project.status,
                    'assignment_id': assignment.id,
                    'start_date': assignment.start_date,
                    'end_date': assignment.end_date,
                    'engagement_type': assignment.engagement_type,
                    'project_teamlead': assignment.project.team_lead.get_full_name if assignment.project.team_lead else None,
                }
                data.append(project_data)

            return JsonResponse({
                'employee_id': user.id,
                'assignments': data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



