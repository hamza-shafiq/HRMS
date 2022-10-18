from assets.permissions import AssetsPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer
