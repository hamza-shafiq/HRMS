from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from finance.permissions import PayrollPermission
from finance.models import Payroll
from finance.serializers import PayRollSerializer


class PayRollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PayrollPermission]
    queryset = Payroll.objects.all()
    serializer_class = PayRollSerializer

    @action(detail=False, url_name="check_payroll", methods=['Get'])
    def check_payroll(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        payroll = Payroll.objects.filter(employee=user.id)
        if payroll:
            serializer = PayRollSerializer(payroll, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'No payroll is created for you yet'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        emp = self.request.query_params.get('emp')

        if month or year or emp:
            try:
                if emp:
                    record = Payroll.objects.filter(employee=emp, is_deleted=False)
                if month:
                    if emp:
                        record = record.filter(month=month)
                    else:
                        record = Payroll.objects.filter(month=month, is_deleted=False)
                if year:
                    if month or emp:
                        record = record.filter(year=year)
                    else:
                        record = Payroll.objects.filter(year=year, is_deleted=False)
            except ValidationError:
                return JsonResponse({'detail': 'Invalid Month Format'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return JsonResponse({'error': 'Invalid Month format'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PayRollSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Payroll.objects.all()
        serializer = PayRollSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
