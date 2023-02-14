from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status, mixins
from assets.models import Asset, AssignedAsset
from employees.models import Employee, Department
from recruitments.models import Recruits
from hrms.permissions import BaseCustomPermission
from attendance.models import Attendance
from datetime import datetime
from employees.serializers import EmployeeSerializer
from attendance.serializers import AttendanceSerializer


class DashboardStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, BaseCustomPermission]
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        emp = self.request.query_params.get('emp')
        if emp:  # emp attendance filter
            try:
                record = Attendance.objects.filter(employee_id=emp, is_deleted=False)
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AttendanceSerializer(record, many=True)
            serializer = serializer.data
        else:
            serializer = []
        total_department = Department.objects.count()
        emp_attendance = serializer
        total_employees = Employee.objects.count()
        present_employees = Employee.objects.filter(employee_status="WORKING", is_active=True).count()
        total_assets = Asset.objects.count()
        assignee = AssignedAsset.objects.count()
        total_recruits = Recruits.objects.count()
        remaining_assets = total_assets - assignee
        pending_recruits = Recruits.objects.filter(status="PENDING").count()
        active_recruits = total_recruits - pending_recruits
        attendees = Attendance.objects.filter(check_in__date=datetime.now().date()).count()
        absent_employees = present_employees - attendees
        data = {"total_departments": total_department, "total_employees": total_employees,
                "present_employees": present_employees, "absent_employees": absent_employees,
                "total_assets": total_assets, "total_assignee": assignee, "remaining_assets": remaining_assets,
                "total_recruits": total_recruits, "active_recruits": active_recruits,
                "pending_recruits": pending_recruits, "total_attendees": attendees, "emp_attendance": emp_attendance}
        return JsonResponse(status=status.HTTP_200_OK, data=data)
