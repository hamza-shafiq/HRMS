from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assets.views import AssetViewSet, AssignedAssetViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename="asset")
router.register(r'assigned-asset', AssignedAssetViewSet, basename="assigned-asset")

urlpatterns = [
    path('', include(router.urls)),
]
