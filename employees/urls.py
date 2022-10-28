from django.urls import include, path
from rest_framework.routers import DefaultRouter

from employees.views import DepartmentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename="department")
router.register(r'employees', EmployeeViewSet, basename="employees")

urlpatterns = [
    path('', include(router.urls)),
]
