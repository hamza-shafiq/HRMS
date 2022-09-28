from .serializers import DepartmentSerializer, EmployeeSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from employees.models import Employee, Department
# Create your views here.


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer