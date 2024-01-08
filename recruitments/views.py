from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hrms.pagination import CustomPageNumberPagination
from recruitments.models import Recruits

from .permissions import RecruitsPermission
from .serializers import RecruitsSerializer


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsPermission]
    queryset = Recruits.objects.filter(is_deleted=False)
    serializer_class = RecruitsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['position', 'status']
    pagination_class = CustomPageNumberPagination
