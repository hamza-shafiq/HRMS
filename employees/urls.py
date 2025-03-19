from django.urls import include, path
from rest_framework.routers import DefaultRouter

from employees.views import DepartmentViewSet, EmployeeViewSet, EmploymentHistoryViewSet, TenureViewSet

router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename="department")
router.register(r'employees', EmployeeViewSet, basename="employees")
router.register(r'employee_history', EmploymentHistoryViewSet, basename="employee_history")
router.register(r'tenure', TenureViewSet, basename="tenure")

urlpatterns = [
    path('', include(router.urls)),
]
