from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset


class AssetViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'admin': True},
        'partial_update': {'admin': True},
        'destroy': {'admin': True},
    }
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssignedAssetViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'admin': True},
        'partial_update': {'admin': True},
        'destroy': {'admin': True},
    }
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer
