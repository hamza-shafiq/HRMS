from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from assets.models import Asset, AssignedAsset
from attendance.models import Attendance, Leaves
from attendance.serializers import AttendanceSerializer, LeaveSerializer
from dashboard.permissions import DashboardPermission
from employees.models import Department, Employee
from employees.serializers import EmployeeSerializer
from recruitments.models import Recruits
from tasks.models import Tasks
from tasks.serializers import TasksSerializer


class DashboardStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, DashboardPermission]
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        emp = self.request.query_params.get('emp')
        if emp:
            try:
                month = datetime.now().month
                record = Attendance.objects.filter(employee_id=emp, check_in__month=month, is_deleted=False)
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
        working_employees = Employee.objects.filter(employee_status="WORKING", is_active=True)
        user = request.user
        total_assets = Asset.objects.count()
        assignee = AssignedAsset.objects.count()
        total_recruits = Recruits.objects.count()
        remaining_assets = total_assets - assignee
        pending_recruits = Recruits.objects.filter(status="PENDING").count()
        active_recruits = total_recruits - pending_recruits
        attendees = Attendance.objects.filter(check_in__date=datetime.now().date()).count()
        absent_employees = present_employees - attendees
        leave_data = Leaves.objects.filter(is_deleted=False).order_by('-request_date')[:3]
        seria = LeaveSerializer(leave_data, many=True)
        seria = seria.data
        working_employee_data = [{"id": emp.id, "name": f"{emp.first_name} {emp.last_name}"} for emp
                                 in working_employees]
        serializer_context = {
            'request': request,
        }
        record = Employee.objects.filter(id=user.id, is_deleted=False)
        serializer = EmployeeSerializer(record, many=True, context=serializer_context)

        data = {"total_departments": total_department, "total_employees": total_employees,
                "present_employees": present_employees, "working_employees": working_employee_data,
                "absent_employees": absent_employees,
                "total_assets": total_assets, "total_assignee": assignee, "remaining_assets": remaining_assets,
                "total_recruits": total_recruits, "active_recruits": active_recruits,
                "pending_recruits": pending_recruits, "total_attendees": attendees, "emp_attendance": emp_attendance,
                "leave_data": seria, "profile_pic": serializer.data[0]['profile_pic'] if serializer.data else None
                }
        return JsonResponse(status=status.HTTP_200_OK, data=data)

    @staticmethod
    def working_days():

        today = datetime.now()

        first_day_of_month = datetime(today.year, today.month, 1)

        dates = (first_day_of_month + timedelta(idx) for idx in range((today - first_day_of_month).days + 1))

        working_days_count = sum(1 for day in dates if day.weekday() < 5)

        return working_days_count

    @action(detail=False, url_path="employee_dashboard", methods=['get'])
    def employee_dashboard(self, request):
        user = request.user
        employee = EmployeeSerializer(Employee.objects.filter(id=user.id))
        leaves_approved = LeaveSerializer(Leaves.objects.filter(status='APPROVED', employee_id=user.id), many=True)
        leaves_approved_dict = employee.get_leaves_dict(leaves_approved)
        if not leaves_approved_dict:
            leaves_approved_dict = {}
        approve_leave_count = sum(
            value for key, value in leaves_approved_dict.items() if key not in ["WORK_FROM_HOME", "EXTRA_DAYS"])

        leaves_rejected = LeaveSerializer(Leaves.objects.filter(status='REJECTED', employee_id=user.id), many=True)
        leaves_rejected_dict = employee.get_leaves_dict(leaves_rejected)
        if not leaves_rejected_dict:
            leaves_rejected_dict = {}
        rejected_leave_count = sum(
            value for key, value in leaves_rejected_dict.items() if key not in ["WORK_FROM_HOME", "EXTRA_DAYS"])

        leaves = LeaveSerializer(Leaves.objects.filter(employee_id=user.id), many=True)
        leaves_dict = employee.get_leaves_dict(leaves)
        if not leaves_dict:
            leaves_dict = {}
        leave_count = sum(
            value for key, value in leaves_dict.items() if key not in ["WORK_FROM_HOME", "EXTRA_DAYS"])
        month = datetime.now().month
        attendees = Attendance.objects.filter(employee_id=user.id, check_in__month=month).count()
        leaves_rejected = rejected_leave_count
        leaves_accepted = approve_leave_count
        total_leaves_applied = leave_count
        working_days = self.working_days()
        total_absents = working_days - attendees
        tasks_data = Tasks.objects.filter(employee=user.id, is_deleted=False).order_by('-deadline')[:3]
        task_seria = TasksSerializer(tasks_data, many=True)
        task_seria = task_seria.data
        serializer_context = {
            'request': request,
        }
        record = Employee.objects.filter(id=user.id, is_deleted=False)
        serializer = EmployeeSerializer(record, many=True, context=serializer_context)

        data = {"employee_present_for_current_month": attendees, "leaves_rejected": leaves_rejected,
                "leaves_approved": leaves_accepted, "total_leaves_applied": total_leaves_applied,
                'total_working_days': working_days, 'total_absents': total_absents, "tasks_data": task_seria,
                "profile_pic": serializer.data[0]['profile_pic'] if serializer.data else None
                }
        return JsonResponse(status=status.HTTP_200_OK, data=data)
