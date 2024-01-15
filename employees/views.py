import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Department, Employee
from employees.permissions import DepartmentPermission, EmployeePermission
from hrms.pagination import CustomPageNumberPagination

from .serializers import DepartmentSerializer, EmployeeSerializer
from django.db.models import Q


class EmployeeFilter(django_filters.FilterSet):
    employee_status = filters.CharFilter(
        method='filter_employee_status',
    )

    department = filters.CharFilter(
        method='filter_by_department',
    )

    full_name = filters.CharFilter(
        method='filter_employee_name',
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'national_id_number',
                  'gender', 'department', 'designation', 'joining_date', 'employee_status', 'full_name']

    def filter_employee_name(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name')).
                filter(full_name__icontains=value))

    def filter_employee_status(self, queryset, name, value):
        return queryset.filter(employee_status=value)

    def filter_by_department(self, queryset, name, value):
        return queryset.filter(department__id=value)


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DepartmentPermission]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=False, url_path="unique-values", methods=['get'])
    def get(self, request, *args, **kwargs):
        # Get unique values of the specific column
        unique_values = Department.objects.values_list('id', 'department_name')

        # Convert the queryset to a list
        unique_values_list = [{'id': item[0], 'department_name': item[1]} for item in unique_values]

        return JsonResponse({'unique_values': unique_values_list})


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, EmployeePermission]
    queryset = Employee.objects.all()
    queryset = queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name'))
    queryset = queryset.order_by('full_name')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=False, url_path="unique-values", methods=['get'])
    def get(self, request, *args, **kwargs):
        # Get unique values of the specific column
        employees = Employee.objects.all()

        # Create a list of dictionaries with 'id' and 'employee_name'
        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        unique_values_list = [{'id': item['id'], 'name': item.get('employee_name')} for item in serializer.data]

        return JsonResponse({'unique_values': unique_values_list})

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
                except ValidationError:
                    return JsonResponse({'detail': 'Invalid employee id'},
                                        status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'error': 'Employee id is not provided'}, status=status.HTTP_204_NO_CONTENT)
        elif user.is_employee:
            record = Employee.objects.filter(id=user.id, is_deleted=False)
            serializer = EmployeeSerializer(record, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'user except admin and employee is not allowed to '
                                      'to perform filter'},
                            status=status.HTTP_403_FORBIDDEN)
