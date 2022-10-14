from rest_framework.settings import api_settings

from assets.permissions import AssetsPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset


class AssetViewSet(viewsets.ModelViewSet):
    # view_permissions = {
    #     'retrieve': {'admin': True, 'employee': True},
    #     'create': {'admin': True},
    #     'list': {'admin': True, 'employee': True},
    #     'update': {'admin': True},
    #
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, AssetsPermission]


class AssignedAssetViewSet(viewsets.ModelViewSet):
    # view_permissions = {
    #     'retrieve': {'admin': True, 'employee': True},
    #     'create': {'admin': True},
    #     'list': {'admin': True, 'employee': True},
    #     'update': {'admin': True},
    # }
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [AssetsPermission]
