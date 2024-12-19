import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Value as V
from django.db.models.functions import Concat, Lower
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Department, Employee, EmployeeHistory
from employees.permissions import DepartmentPermission, EmployeeHistoryPermission, EmployeePermission
from hrms.pagination import CustomPageNumberPagination

from .serializers import DepartmentSerializer, EmployeeSerializer, EmploymentHistorySerializer


class EmployeeFilter(django_filters.FilterSet):
    employee_status = filters.CharFilter(method='filter_employee_status')
    department = filters.CharFilter(method='filter_by_department')
    full_name = filters.CharFilter(method='filter_employee_name')

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone_number', 'national_id_number',
                  'gender', 'department', 'designation', 'joining_date', 'employee_status', 'full_name',
                  'team_lead']

    def filter_employee_name(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name')).
                filter(full_name__icontains=value))

    def filter_employee_status(self, queryset, name, value):
        return queryset.filter(employee_status=value)

    def filter_by_department(self, queryset, name, value):
        return queryset.filter(department__id=value)

    def filter_queryset(self, queryset):
        portal = self.request.query_params.get('portal')
        user = self.request.user
        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = queryset.filter(team_lead=user.id)
        return super().filter_queryset(queryset)


class EmployeeHistoryFilter(django_filters.FilterSet):
    emp_id = filters.CharFilter(
        method='filter_employee_id',
    )

    class Meta:
        model = EmployeeHistory
        fields = ["id", "employee", "subject", "remarks", "increment", "interval_from", "interval_to", "review_by",
                  "review_date", "added_by", "added_date"]

    def filter_employee_id(self, queryset, name, value):
        return queryset.filter(employee__id=value)


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
    queryset = Employee.objects.all().order_by(Lower('first_name'))
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    serializer_class = EmployeeSerializer
    pagination_class = CustomPageNumberPagination

    def update(self, request, *args, **kwargs):
        employee = self.get_object()
        lead = request.data.get('team_lead')
        old_lead = employee.team_lead

        try:
            # Handle team lead change
            if lead:
                lead_employee = Employee.objects.get(id=lead)
                employee.team_lead = lead_employee
                lead_employee.is_team_lead = True
                employee.save()
                lead_employee.save()

            elif not lead and employee.team_lead:
                employee.team_lead = None
                employee.save()

            if old_lead and not Employee.objects.filter(team_lead=old_lead.id).exists():
                old_lead.is_team_lead = False
                old_lead.save()

            # Update the rest of the employee data
            serializer = EmployeeSerializer(employee, data=request.data, partial=True, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Employee.DoesNotExist:
            return Response({'error': 'Team lead not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid team lead ID'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="unique-values", methods=['get'])
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_admin:
            employees = Employee.objects.all()
        else:
            employee = Employee.objects.get(id=user.id)
            if employee.is_team_lead:
                employees = Employee.objects.filter(team_lead=user.id)
            else:
                employees = Employee.objects.filter(id=user.id)

        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        return JsonResponse({'unique_values': serializer.data})

    @action(detail=False, url_path="team_leads", methods=['get'])
    def get_team_leads(self, request, *args, **kwargs):
        team_lead_employees = Employee.objects.filter(is_team_lead=True)
        serializer = EmployeeSerializer(team_lead_employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path="get_employee", methods=['get'])
    def employee_detail(self, request):
        user = request.user
        serializer_context = {'request': request}

        if user.is_admin and self.request.query_params.get('employee_id'):
            emp_id = self.request.query_params.get('employee_id')
            if emp_id:
                try:
                    emp_record = None
                    if emp_id is not None and Employee.objects.filter(id=emp_id, is_deleted=False).exists():
                        emp_record = Employee.objects.get(id=emp_id, is_deleted=False)
                    tl_employees = Employee.objects.filter(team_lead=emp_id, is_deleted=False)
                    if emp_record is not None:
                        tl_serializer = EmployeeSerializer(emp_record, context=serializer_context)
                        serializer_context = {'request': request, 'minimal_fields': True}
                        tl_employees_serializer = EmployeeSerializer(tl_employees, many=True,
                                                                     context=serializer_context)
                        return Response({"employee": tl_serializer.data,
                                         "employees": tl_employees_serializer.data}, status=status.HTTP_200_OK)
                    return JsonResponse({'error': f'Employee with id: {emp_id} does not exist'},
                                        status=status.HTTP_404_NOT_FOUND)
                except ValidationError:
                    return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'error': 'Employee id is not provided'}, status=status.HTTP_204_NO_CONTENT)

        elif user.is_admin:
            record = Employee.objects.all()
            serializer = EmployeeSerializer(record, many=True, context=serializer_context)
            return Response({"employees": serializer.data}, status=status.HTTP_200_OK)
        else:
            if user.employee.is_team_lead and self.request.query_params.get('employee_id'):
                emp_id = self.request.query_params.get('employee_id')
                if emp_id:
                    try:
                        record = Employee.objects.get(id=emp_id, is_deleted=False)
                        if record is not None:
                            serializer = EmployeeSerializer(record, context=serializer_context)
                            return Response({"employee": serializer.data}, status=status.HTTP_200_OK)
                        return JsonResponse({'error': f'Employee with id: {emp_id} does not exist'},
                                            status=status.HTTP_404_NOT_FOUND)
                    except ValidationError:
                        return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
                return JsonResponse({'error': 'Employee id is not provided'}, status=status.HTTP_204_NO_CONTENT)

            elif not user.employee.is_team_lead:
                record = Employee.objects.get(id=user.id, is_deleted=False)
                serializer = EmployeeSerializer(record, context=serializer_context)
                return Response({"employee": serializer.data}, status=status.HTTP_200_OK)
            elif user.employee.is_team_lead:
                record = Employee.objects.filter(team_lead=user.id, is_deleted=False)
                serializer = EmployeeSerializer(record, many=True, context=serializer_context)
                return Response({"employee": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'User not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)


class EmploymentHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, EmployeeHistoryPermission]
    queryset = EmployeeHistory.objects.all()
    serializer_class = EmploymentHistorySerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = EmployeeHistoryFilter
