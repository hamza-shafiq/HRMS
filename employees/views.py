from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DepartmentSerializer, EmployeeSerializer
from rest_framework import viewsets, status
from employees.models import Employee, Department
from django_filters import rest_framework as filters


class EmployeeFilter(filters.FilterSet):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'national_id_number',
                  'gender', 'department', 'designation', 'joining_date']


class DepartmentViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'admin': True},
        'destroy': {'admin': True},
    }
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def destroy(self, request, *args, **kwargs):
        department = self.get_object()
        department.is_deleted = True
        department.save()
        return JsonResponse({'success': f'Department {department.department_name} deleted successfully'}, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'admin': True},
        'list': {'admin': True},
        'update': {'admin': True},
        'destroy': {'admin': True},
    }
    queryset = Employee.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer

    @action(detail=False, url_path="get_employee")
    def employee_detail(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        if user.is_superuser:
            emp_id = self.request.query_params.get('employee_id')
            if emp_id:
                try:
                    record = Employee.objects.filter(id=emp_id)
                    if record:
                        serializer = EmployeeSerializer(record, many=True, context=serializer_context)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return JsonResponse({'error': f'Employee with id: {emp_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return JsonResponse({'error': 'Invalid employee id'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return JsonResponse({'error': 'Employee id is not provided'}, status=status.HTTP_204_NO_CONTENT)
        elif user.is_employee:
            record = Employee.objects.filter(id=user.id)
            if record:
                serializer = EmployeeSerializer(record, many=True, context=serializer_context)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'Only admin and employee can see any employee details'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.is_deleted = True
        employee.is_active = False
        employee.save()
        return JsonResponse({'success': f'Employee {employee.first_name} {employee.last_name} deleted successfully'}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = Employee.objects.filter(is_deleted=False)
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

