from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from assets.models import Asset, AssignedAsset
from assets.permissions import AssetsPermission
from assets.serializers import AssetSerializer, AssignedAssetSerializer


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def list(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        asset = []
        choice = self.request.query_params.get('choice')
        if choice == 'ASSIGNED':
            assign = list(AssignedAsset.objects.filter(is_deleted=False).values_list('asset', flat=True))

            assets = Asset.objects.filter(id__in=assign, is_deleted=False)
            serializer = AssetSerializer(assets, many=True, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif choice == 'AVAILABLE':
            assign_ids = list(AssignedAsset.objects.filter(is_deleted=False).values_list('asset_id', flat=True))
            available_assets = Asset.objects.filter(is_deleted=False).exclude(id__in=assign_ids)
            serializer = AssetSerializer(available_assets, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Asset.objects.filter(is_deleted=False)
        serializer = AssetSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AssetsPermission]
    queryset = AssignedAsset.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['employee_id']
    serializer_class = AssignedAssetSerializer
