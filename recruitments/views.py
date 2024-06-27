from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hrms.pagination import CustomPageNumberPagination
from recruitments.models import Recruits, RecruitsHistory
from tasks.serializers import TasksSerializer

from .permissions import RecruitsHistoryPermission, RecruitsPermission
from .serializers import RecruitsHistorySerializer, RecruitsSerializer


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsPermission]
    queryset = Recruits.objects.filter(is_deleted=False)
    serializer_class = RecruitsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['position', 'status']
    pagination_class = CustomPageNumberPagination

    def create_task_for_interview(self, data, assigned_by):
        if len(data['interview_date']) and len(data['assigned_to']):
            task_data = {
                "title": "Interview",
                "deadline": data['interview_date'],
                "employee": data['assigned_to'],
                "description": (
                    f"Interview Scheduled for {data['first_name']} {data['last_name']} "
                    f"on {data['interview_date']}"
                ),

                "assigned_by": assigned_by,
            }
            task_serializer = TasksSerializer(data=task_data)
            task_serializer.is_valid(raise_exception=True)
            task_serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        self.create_task_for_interview(data, request.user)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        self.create_task_for_interview(data, request.user)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RecruitsHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsHistoryPermission]
    queryset = RecruitsHistory.objects.filter(is_deleted=False)
    serializer_class = RecruitsHistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['recruit_id']
    pagination_class = CustomPageNumberPagination
