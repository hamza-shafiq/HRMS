from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import AttendanceViewSet, LeavesViewSet, AttendanceRequestViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename="attendance")
router.register(r'leaves', LeavesViewSet, basename="leaves")
router.register(r'attendance-request', AttendanceRequestViewSet, basename='attendance-request')


urlpatterns = [
    path('', include(router.urls)),
]
