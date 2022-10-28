from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recruitments.views import RecruitsViewSet

router = DefaultRouter()
router.register(r'recruits', RecruitsViewSet, basename="recruits")

urlpatterns = [
    path('', include(router.urls)),
]
