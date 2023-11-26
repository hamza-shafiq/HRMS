from django.urls import include, path
from rest_framework import routers

from dashboard.views import DashboardStatsViewSet

router = routers.DefaultRouter()
router.register(r'dashboard', DashboardStatsViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
