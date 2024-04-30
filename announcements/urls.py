from django.urls import include, path
from rest_framework.routers import DefaultRouter

from announcements.views import AnnouncementsViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementsViewSet, basename="announcements")

urlpatterns = [
    path('', include(router.urls)),
]
