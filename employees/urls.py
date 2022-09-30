from django.urls import path
from employees.views import DepartmentViewSet, EmployeeViewSet

department_list = DepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
department_detail = DepartmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
employees_list = EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
employees_detail = EmployeeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('department/', department_list, name="department-list"),
    path('department/<str:pk>/', department_detail, name='department-detail'),
    path('employees/', employees_list, name="employees-list"),
    path('employees/<str:pk>/', employees_detail, name='employees-detail'),
]