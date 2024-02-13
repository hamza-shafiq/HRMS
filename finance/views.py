import django_filters
import pandas as pd
from django.conf import settings
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Employee
from finance.models import Payroll
from finance.permissions import PayrollPermission
from finance.serializers import PayRollSerializer
from finance.utils import normalize_header
from hrms.pagination import CustomPageNumberPagination
from user.tasks import send_email


class PayrollFilter(django_filters.FilterSet):
    employee = filters.CharFilter(
        method='filter_employee_id',
    )

    year = filters.CharFilter(
        method='filter_year',
    )

    month = filters.CharFilter(
        method='filter_month'
    )

    class Meta:
        model = Payroll
        fields = ["id", "basic_salary", "bonus", "reimbursement", "travel_allowance", "tax_deduction",
                  "month", "year", "released", "employee"]

    def filter_year(self, queryset, name, value):
        return queryset.filter(year=value)

    def filter_month(self, queryset, name, value):
        return queryset.filter(month=value)

    def filter_employee_id(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('employee__first_name', V(' '), 'employee__last_name')).
                filter(full_name__icontains=value))


class PayRollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PayrollPermission]
    queryset = Payroll.objects.all().order_by('-created')
    serializer_class = PayRollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPageNumberPagination
    filterset_class = PayrollFilter

    @action(detail=False, url_name="check_payroll", methods=['Get'])
    def check_payroll(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        payroll = Payroll.objects.filter(employee=user.id, is_deleted=False).order_by('-created')

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(payroll, request)
        if payroll:
            serializer = PayRollSerializer(result_page, many=True, context=serializer_context)
            return paginator.get_paginated_response(serializer.data)
        return JsonResponse({'detail': 'No payroll is created for you yet'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_name="import-payrolls-data", methods=['Post'])
    def import_payroll_details(self, request):
        file = request.FILES.get('payroll_sheet')
        month = request.data.get('month', None)
        year = request.data.get('year', None)
        if not file:
            return Response({'error': 'No file was provided'}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_excel(file, skiprows=4)
        new_headers = normalize_header(list(df.columns))
        df.rename(columns=dict(zip(list(df.columns), new_headers)), inplace=True)
        df.rename(columns={'salary_net_of_deductions_+_income_tax': 'salary'}, inplace=True)
        df.fillna(0, inplace=True)

        emails_to_update = df['email_ids'].tolist()
        employees = Employee.objects.filter(email__in=emails_to_update).values_list('id', 'email')
        emp_dt = {str(emp[1]): str(emp[0]) for emp in employees}
        payroll_list = []
        for index, row in df.iterrows():
            email = row['email_ids']
            if email in emp_dt:
                employee_id = emp_dt[email]
                bonus = row['late_sitting_bonus'] + row['increment'] + row['project_bonus'] + row[
                    'project_commission'] + row['overtime']
                basic_salary = row['basic_salary']
                travel_allowance = row['allowance']
                tax_deductions = row['tax_deductions'] + row['deductions']
                reimbursement = row['arrears']
                config = {
                    'loan_advance': row['loan_advance'],
                    'overtime': row['overtime'],
                    'increment': row['increment'],
                    'late_sitting_bonus': row['late_sitting_bonus'],
                    'arrears': row['arrears'],
                    'allowance': row['allowance'],
                    'project_bonus': row['project_bonus'],
                    'project_commission': row['project_commission'],
                    'deductions': row['deductions'],
                    'tax_deductions': row['tax_deductions'],
                    'total_salary': row['salary']
                }
                year = year
                month = month

                payroll = Payroll(
                    employee_id=employee_id,
                    bonus=bonus,
                    basic_salary=basic_salary,
                    travel_allowance=travel_allowance,
                    tax_deduction=tax_deductions,
                    reimbursement=reimbursement,
                    config=config,
                    month=month,
                    year=year,
                )
                payroll_list.append(payroll)
        Payroll.objects.bulk_create(payroll_list)

        return Response({'message': 'Payroll details imported successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, url_name="send-mail", methods=['Post'])
    def send_mail(self, request):
        instance_id = request.data.get('id', None)
        released = request.data.get('released', None)
        employee_id = request.data.get('employee', None)
        month = request.data.get('month', None)
        year = request.data.get('year', None)
        payroll = Payroll.objects.get(id=instance_id)
        employee = Employee.objects.filter(id=employee_id).values_list('id', 'first_name', 'last_name', 'email')
        emp_dt = {str(emp[0]): [f'{emp[1]} {emp[2]}', emp[3]] for emp in employee}
        payroll_base_url = "payrolls/emp_payrolls"
        data = {
            'to_email': emp_dt[employee_id][1],
            'email_subject': 'Payroll Released'
        }
        if not released:
            payroll.released = True
            payroll.save()
            email_body = 'Hi ' + emp_dt[employee_id][0] + '!\n' + \
                         '\nYour payroll has been generated for the month of ' + month \
                         + ' ' + year + '\n' + \
                         'You can now view it at your dashboard.' + \
                         f'\n{settings.CLIENT_URL + payroll_base_url}'
            data['email_subject'] = 'Payroll Generated'
            data['email_body'] = email_body
            send_email.delay(data)
            return Response({'message': 'Salary released Successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Salary is being processed will be Updated Soon'}, status=status.HTTP_200_OK)
