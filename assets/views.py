from django.http import JsonResponse
from assets.permissions import AssetsPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from assets.models import Asset, AssignedAsset
from django_filters import rest_framework as filters


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def destroy(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.is_deleted = True
        asset.save()
        return JsonResponse({'success': f'Asset with model: {asset.asset_model} deleted successfully'},
                            status=status.HTTP_200_OK)


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = AssignedAsset.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['employee_id']
    serializer_class = AssignedAssetSerializer

    def destroy(self, request, *args, **kwargs):
        assigned_asset = self.get_object()
        assigned_asset.is_deleted = True
        assigned_asset.save()
        return JsonResponse({'success': 'Asset has been removed'}, status=status.HTTP_200_OK)
