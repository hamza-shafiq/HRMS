from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset


class AssetViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'admin': True},
    }
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssignedAssetViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'admin': True},
    }
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer
