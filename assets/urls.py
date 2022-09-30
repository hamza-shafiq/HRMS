from django.urls import path
from assets.views import AssetViewSet, AssignedAssetViewSet

asset_list = AssetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
asset_detail = AssetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
assigned_asset_list = AssignedAssetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
assigned_asset_detail = AssignedAssetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('assets/', asset_list, name="asset-list"),
    path('assets/<str:pk>/', asset_detail, name='asset-detail'),
    path('assigned_assets/', assigned_asset_list, name="assigned-asset-list"),
    path('assigned_assets/<str:pk>/', assigned_asset_detail, name='assigned-asset-detail'),
]