from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Department, Employee
from employees.permissions import DepartmentPermission, EmployeePermission

from .serializers import DepartmentSerializer, EmployeeSerializer


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

    @action(detail=False, url_path="get_employee", methods=['get'])
    def employee_detail(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        if user.is_admin:
            emp_id = self.request.query_params.get('employee_id')
            if emp_id:
                try:
                    record = Employee.objects.filter(id=emp_id, is_deleted=False)
                    if record:
                        serializer = EmployeeSerializer(record, many=True, context=serializer_context)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return JsonResponse({'error': f'Employee with id: {emp_id} does not exist'},
                                        status=status.HTTP_404_NOT_FOUND)
                except:
                    return JsonResponse({'error': 'Invalid employee id'}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({'error': 'Employee id is not provided'}, status=status.HTTP_204_NO_CONTENT)
        elif user.is_employee:
            record = Employee.objects.filter(id=user.id, is_deleted=False)
            serializer = EmployeeSerializer(record, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'user except admin and employee is not allowed to '
                                      'to perform filter'},
                            status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        queryset = Employee.objects.filter(is_deleted=False)
        serializer = EmployeeSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
