from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from assets.filters import AssetFilter
from assets.models import Asset, AssignedAsset
from assets.permissions import AssetsPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer
from hrms.pagination import CustomPageNumberPagination


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AssetFilter
    pagination_class = CustomPageNumberPagination


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = AssignedAsset.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['employee_id']
    serializer_class = AssignedAssetSerializer
