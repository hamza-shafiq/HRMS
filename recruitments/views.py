from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hrms.pagination import CustomPageNumberPagination
from recruitments.models import Recruits, RecruitsHistory

from .permissions import RecruitsPermission, RecruitsHistoryPermission
from .serializers import RecruitsSerializer, RecruitsHistorySerializer


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsPermission]
    queryset = Recruits.objects.filter(is_deleted=False)
    serializer_class = RecruitsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['position', 'status']
    pagination_class = CustomPageNumberPagination


class RecruitsHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsHistoryPermission]
    queryset = RecruitsHistory.objects.filter(is_deleted=False)
    serializer_class = RecruitsHistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['id']
    pagination_class = CustomPageNumberPagination
