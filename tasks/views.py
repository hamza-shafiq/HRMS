import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from hrms.pagination import CustomPageNumberPagination
from tasks.models import Tasks
from rest_framework.decorators import action
from django.db.models import Value as V
from django.db.models.functions import Concat
from rest_framework.response import Response

from .permissions import TasksPermission
from tasks.serializers import TasksSerializer


class TaskFilter(django_filters.FilterSet):
    employee_name = filters.CharFilter(
        method='filter_employee_id',
    )

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'assigned_by', 'employee', 'deadline', 'created_on', 'status']

    def filter_employee_id(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('employee__first_name', V(' '), 'employee__last_name')).
                filter(full_name__icontains=value))


class TasksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TasksPermission]
    queryset = Tasks.objects.all().order_by('-created_on')
    serializer_class = TasksSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter
    filterset_field = ['employee_id', 'status']
    pagination_class = CustomPageNumberPagination

    @action(detail=True, url_name="update-status", methods=['PATCH'])
    def update_status(self, request, pk):
        task = self.get_object()
        if 'status' in request.data:
            task.status = request.data['status']
            task.save()
        return Response(status=status.HTTP_200_OK, data=TasksSerializer(task,
                        context=self.get_serializer_context()).data)
