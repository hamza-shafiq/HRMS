from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import AttendanceViewSet, LeavesViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename="attendance")
router.register(r'leaves', LeavesViewSet, basename="leaves")


urlpatterns = [
    path('', include(router.urls)),
]
