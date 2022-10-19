from .serializers import DepartmentSerializer, EmployeeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from employees.permissions import DepartmentPermission, EmployeePermission
from employees.models import Employee, Department
from django_filters import rest_framework as filters


class EmployeeFilter(filters.FilterSet):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'national_id_number',
                  'gender', 'department', 'designation', 'joining_date']


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DepartmentPermission]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, EmployeePermission]
    queryset = Employee.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer
