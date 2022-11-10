from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, mixins
from assets.models import Asset, AssignedAsset
from employees.models import Employee, Department
from recruitments.models import Recruits
from hrms.permissions import BaseCustomPermission
from attendance.models import Attendance
from datetime import datetime
from employees.serializers import EmployeeSerializer


class DashboardStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, BaseCustomPermission]
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        total_department = Department.objects.count()
        total_employees = Employee.objects.count()
        present_employees = Employee.objects.filter(employee_status="WORKING", is_active=True).count()
        total_assets = Asset.objects.count()
        assignee = AssignedAsset.objects.count()
        total_recruits = Recruits.objects.count()
        pending_recruits = Recruits.objects.filter(status="PENDING").count()
        attendees = Attendance.objects.filter(check_in__date=datetime.now().date()).count()
        data = {"total departments": total_department, "total employees": total_employees,
                "present employees": present_employees, "total assets": total_assets,
                "total assignee": assignee, "total recruits": total_recruits,
                "pending recruits": pending_recruits, "total attendees": attendees}
        return JsonResponse(status=status.HTTP_200_OK, data=data)
