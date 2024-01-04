from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hrms.pagination import CustomPageNumberPagination
from policies.models import Policies

from .permissions import PolicyPermission
from .serializers import PolicySerializer


class PoliciesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PolicyPermission]
    queryset = Policies.objects.filter(is_deleted=False)
    serializer_class = PolicySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['file_name']
    pagination_class = CustomPageNumberPagination
