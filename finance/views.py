from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from finance.permissions import PayrollPermission
from django_filters import rest_framework as filters
from finance.models import Payroll
from finance.serializers import PayRollSerializer
from finance.utils import normalize_header
from employees.models import Employee
import pandas as pd


class PayRollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PayrollPermission]
    queryset = Payroll.objects.all().order_by('-created')
    serializer_class = PayRollSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_fields = ['employee', 'month', 'year']

    @action(detail=False, url_name="check_payroll", methods=['Get'])
    def check_payroll(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        payroll = Payroll.objects.filter(employee=user.id, is_deleted=False).order_by('-created')
        if payroll:
            serializer = PayRollSerializer(payroll, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'No payroll is created for you yet'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_name="import-payrolls-data", methods=['Post'])
    def import_payroll_details(self, request):
        file = request.FILES.get('file')

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
                bonus = row['late_sitting_bonus'] + row['increment'] + row['project_bonus'] + row['project_commission']
                basic_salary = row['basic_salary']
                travel_allowance = row['travel_allowance']
                tax_deductions = row['tax_deductions']
                reimbursement = row['other_deductions']
                year = row['year']

                payroll = Payroll(
                    employee_id=employee_id,
                    bonus=bonus,
                    basic_salary=basic_salary,
                    travel_allowance=travel_allowance,
                    tax_deduction=tax_deductions,
                    reimbursement=reimbursement,
                    year=year,
                )
                payroll_list.append(payroll)
        Payroll.objects.bulk_create(payroll_list)

        return Response({'message': 'Payroll details imported successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, url_name="send-mail", methods=['Post'])
    def send_mail(self):
        pass
