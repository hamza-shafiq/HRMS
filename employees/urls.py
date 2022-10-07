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
list_all_employees = EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
employees_detail = EmployeeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

get_employee_details = EmployeeViewSet.as_view({
    'get': 'employee_detail'
})

urlpatterns = [
    path('department/', department_list, name="department-list"),
    path('department/<str:pk>/', department_detail, name='department-detail'),
    path('employees/', list_all_employees, name="employees-list"),
    path('employees/<str:pk>/', employees_detail, name='employees-detail'),
    path('employee-detail/', get_employee_details, name='get_employee'),
]