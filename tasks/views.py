from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hrms.pagination import CustomPageNumberPagination
from tasks.models import Tasks
from rest_framework.decorators import action

from .permissions import TasksPermission
from tasks.serializers import TasksSerializer


class TasksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TasksPermission]
    queryset = Tasks.objects.filter(is_deleted=False)
    serializer_class = TasksSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPageNumberPagination
