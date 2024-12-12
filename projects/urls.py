from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projects.views import ProjectsViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename="projects")
router.register(r'assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
