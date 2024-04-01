from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TasksViewSet

router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename="tasks")

urlpatterns = [
    path('', include(router.urls)),
]
