from .serializers import DepartmentSerializer, EmployeeSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from employees.models import Employee, Department
from django_filters import rest_framework as filters
from rest_framework_roles.granting import is_self

class EmployeeFilter(filters.FilterSet):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'national_id_number',
                  'gender', 'department', 'designation', 'joining_date']


class DepartmentViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'anon': True},
        'create': {'admin': True},
        'list': {'anon': True},
        'update': {'admin': True},
    }
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Employee.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer
