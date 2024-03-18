from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recruitments.views import RecruitsViewSet, RecruitsHistoryViewSet

router = DefaultRouter()
router.register(r'recruits', RecruitsViewSet, basename="recruits")
router.register(r'recruits_history', RecruitsHistoryViewSet, basename="recruits_history")

urlpatterns = [
    path('', include(router.urls)),
]
