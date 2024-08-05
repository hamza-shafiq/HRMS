from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        emp = request.query_params.get('emp')
        team_lead_id = request.user.id if request.user.is_team_lead else None

        att_serializer = self.get_attendance_data(emp)
        leave_serializer = self.get_leave_data(team_lead_id)

        if team_lead_id:
            data = self.get_team_lead_data(team_lead_id, att_serializer, leave_serializer)
        else:
            data = self.get_admin_data(att_serializer, leave_serializer, request)

        return JsonResponse(status=status.HTTP_200_OK, data=data)

    def get_attendance_data(self, emp):
        if emp:
            try:
                month = datetime.now().month
                record = Attendance.objects.filter(employee_id=emp, check_in__month=month, is_deleted=False)
                return AttendanceSerializer(record, many=True).data
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
        return []

    def get_leave_data(self, team_lead_id):
        if team_lead_id:
            try:
                record = Leaves.objects.filter(employee__team_lead_id=team_lead_id, is_deleted=False).order_by(
                    '-request_date')[:3]
                return LeaveSerializer(record, many=True).data
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            record = Leaves.objects.filter(is_deleted=False).order_by('-request_date')[:3]
            return LeaveSerializer(record, many=True).data

    def get_team_lead_data(self, team_lead_id, att_serializer, leave_serializer):
        emp_attendance = att_serializer

        employees_details = Employee.objects.filter(team_lead=team_lead_id, is_active=True)
        employee_data = [{"id": emp.id, "name": f"{emp.first_name} {emp.last_name}"} for emp in employees_details]

        total_employees = Employee.objects.filter(team_lead=team_lead_id).count()
        present_employees = Employee.objects.filter(employee_status="WORKING", team_lead=team_lead_id,
                                                    is_active=True).count()
        attendees = Attendance.objects.filter(check_in__date=datetime.now().date()).count()
        absent_employees = present_employees - attendees

        return {
            "total_employees": total_employees,
            "active_employees": present_employees,
            "employees_details": employee_data,
            "absent_employees": absent_employees,
            "present_employees": attendees,
            "emp_attendance": emp_attendance,
            "leave_data": leave_serializer
        }

    def get_admin_data(self, att_serializer, leave_serializer, request):
        emp_attendance = att_serializer
        total_department = Department.objects.count()
        total_employees = Employee.objects.count()
        present_employees = Employee.objects.filter(employee_status="WORKING", is_active=True).count()
        working_employees = Employee.objects.filter(employee_status="WORKING", is_active=True)
        total_assets = Asset.objects.count()
        assignee = AssignedAsset.objects.count()
        total_recruits = Recruits.objects.count()
        remaining_assets = total_assets - assignee
        pending_recruits = Recruits.objects.filter(status="PENDING").count()
        active_recruits = total_recruits - pending_recruits
        attendees = Attendance.objects.filter(check_in__date=datetime.now().date()).count()
        absent_employees = present_employees - attendees

        working_employee_data = [{"id": emp.id, "name": f"{emp.first_name} {emp.last_name}"} for emp in
                                 working_employees]
        serializer_context = {'request': request}
        record = Employee.objects.filter(id=request.user.id, is_deleted=False)
        profile_pic = EmployeeSerializer(record, many=True, context=serializer_context).data[0].get(
            'profile_pic') if record else None

        return {
            "total_departments": total_department,
            "total_employees": total_employees,
            "present_employees": present_employees,
            "working_employees": working_employee_data,
            "absent_employees": absent_employees,
            "total_assets": total_assets,
            "total_assignee": assignee,
            "remaining_assets": remaining_assets,
            "total_recruits": total_recruits,
            "active_recruits": active_recruits,
            "pending_recruits": pending_recruits,
            "total_attendees": attendees,
            "emp_attendance": emp_attendance,
            "leave_data": leave_serializer,
            "profile_pic": profile_pic
        }

    @action(detail=False, url_path="team_lead_dashboard", methods=['get'])
    def team_lead_dashboard(self, request):
        user = request.user
        team_lead_id = user.id

        # Ensure the user is a team lead
        if not user.is_team_lead:
            return Response({"detail": "User is not a team lead"}, status=status.HTTP_403_FORBIDDEN)

        try:

            # Fetch employees under the team lead
            employees_details = Employee.objects.filter(team_lead=team_lead_id, is_active=True)
            employee_data = [{"id": emp.id, "name": f"{emp.first_name} {emp.last_name}"} for emp in employees_details]
            # total_employees = Employee.objects.filter(team_lead=team_lead_id).count()

            present_employees = Employee.objects.filter(employee_status="WORKING", team_lead=team_lead_id,
                                                        is_active=True).count()
            attendees = Attendance.objects.filter(employee__team_lead_id=team_lead_id,
                                                  check_in__date=datetime.now().date()).count()
            absent_employees = present_employees - attendees

            # Fetch the last three leave records for employees under the team lead
            leave_records = Leaves.objects.filter(employee__team_lead_id=team_lead_id, is_deleted=False).order_by(
                '-request_date')[:3]
            leave_serializer = LeaveSerializer(leave_records, many=True)

            # Fetch attendance data for employees under the team lead
            attendance_records = Attendance.objects.filter(employee__team_lead_id=team_lead_id, is_deleted=False)
            attendance_serializer = AttendanceSerializer(attendance_records, many=True)

            data = {
                "employees_details": employee_data,
                "total_employees": user.employee.total_employees(),
                "active_employees": present_employees,
                "absent_employees": absent_employees,
                "total_attendees": attendees,
                "emp_attendance": attendance_serializer.data,
                "leave_data": leave_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)

        except ValidationError:
            return Response({"detail": "Invalid team lead id"}, status=status.HTTP_404_NOT_FOUND)

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
