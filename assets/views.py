from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from assets.models import Asset, AssignedAsset
# Create your views here.


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = AssignedAsset.objects.all()
    serializer_class = AssignedAssetSerializer