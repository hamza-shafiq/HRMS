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
from employees.models import Employee


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






