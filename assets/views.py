from assets.permissions import AssetsPermission, AssignedAssetPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssignedAssetPermission]
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer
