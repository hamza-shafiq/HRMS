from datetime import datetime, timedelta

import django_filters
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance, Leaves, AttendanceRequest
from attendance.permissions import AttendancePermission, LeavesPermission, AttendanceRequestPermission
from attendance.serializers import AttendanceSerializer, LeaveSerializer, AttendanceRequestSerializer
from attendance.utils import send_leave_request_message
from employees.models import Employee
from hrms.pagination import CustomPageNumberPagination
from django.utils.timezone import make_aware


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AttendancePermission]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=False, url_name="get-attendance", methods=['Get'])
    def get_attendance(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        attendance = Attendance.objects.filter(employee=user.id).order_by('-check_in')

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(attendance, request)
        if attendance:
            serializer = AttendanceSerializer(result_page, many=True, context=serializer_context)
            return paginator.get_paginated_response(serializer.data)
        return JsonResponse({'detail': 'You did not check-in today'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path="mark-attendance", methods=['post'])
    def mark_attendance(self, request):
        action_type = request.data.get("action", None)
        user = request.user
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.strptime(current_datetime, '%Y-%m-%d %H:%M:%S')
        record = Attendance.objects.filter(employee_id=user.id, check_in__contains=current_datetime.date()).first()
        if hasattr(user, 'employee'):
            if action_type == "check-in":
                if not record:
                    config = {}
                    timer = [{'timer_value': ''}]
                    sessions = [{'start_time': str(current_datetime)}]
                    config['sessions'] = sessions
                    config['timer'] = timer
                    Attendance.objects.create(employee_id=user.id, check_in=current_datetime, config=config,
                                              status="ON_TIME")
                    return JsonResponse({"success": "Employee checked-in successfully!"},
                                        status=status.HTTP_201_CREATED)

                return JsonResponse({"detail": "Employee already checked-in today!"},
                                    status=status.HTTP_208_ALREADY_REPORTED)

            elif action_type == "check-out":
                if not record:
                    return JsonResponse({"detail": "Employee did not check-in today!"},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
                config = record.config
                sessions = config.get('sessions', [])
                if sessions:
                    sessions[-1]['end_time'] = str(current_datetime)
                else:
                    return JsonResponse({"detail": "Session Not found!"}, status=status.HTTP_400_BAD_REQUEST)
                total_time = request.data.get("total_time")
                record.total_time = total_time
                record.check_out = current_datetime
                record.save()
                return JsonResponse({"success": "Employee checked-out successfully!"}, status=status.HTTP_200_OK)

            elif action_type == "pause":
                timer_value = request.data.get('timer', None)
                if not record:
                    return JsonResponse({"detail": "Employee did not check-in today!"},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
                config = record.config
                timer = config.get('timer', [])
                sessions = config.get('sessions', [])
                if sessions:
                    sessions[-1]['end_time'] = str(current_datetime)
                    timer[-1]['timer_value'] = timer_value
                record.save()
                return JsonResponse({"success": "Timer paused successfully!"}, status=status.HTTP_200_OK)

            elif action_type == "resume":
                if not record:
                    return JsonResponse({"detail": "Employee did not check-in today!"},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
                config = record.config
                timer = config.get('timer', [])
                sessions = config.get('sessions', [])
                if sessions:
                    try:
                        paused_at = sessions[-1]['end_time']
                    except:
                        return JsonResponse({"error": "Timer Wasn't Paused!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    timer_value = timer[-1]['timer_value']
                    sessions.append({'start_time': str(current_datetime)})
                    timer.append({'timer_value': ''})
                    record.save()
                    return JsonResponse({"success": "Timer resumed successfully!",
                                         "paused_at": paused_at,
                                         "timer_value": timer_value},
                                        status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"detail": "Sessions Not Found!"}, status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse({"error": "Please enter valid action (check-in/check-out)"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse({"error": "Only employee can mark the attendance"},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, url_path="check-today-attendance", methods=['get'])
    def check_today_attendance(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        attendance = Attendance.objects.filter(employee=user.id, check_in__date=datetime.now().date())
        if attendance:
            serializer = AttendanceSerializer(attendance, many=True, context=serializer_context)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'You did not check-in today'}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        date = self.request.query_params.get('date')
        emp_id = self.request.query_params.get('employee_id')
        portal = self.request.query_params.get('portal')
        user = request.user

        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = Attendance.objects.filter(employee__team_lead=user.id).order_by('-check_in')

        elif not user.is_admin:
            employee = Employee.objects.get(id=user.id)
            if employee.is_team_lead:
                team_lead = employee
                try:
                    queryset = Attendance.objects.filter(employee__team_lead=team_lead).order_by('-check_in')
                except ValueError:
                    return JsonResponse({'error': 'invalid team Lead'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Attendance.objects.all().order_by('-check_in')
        if date or emp_id:
            try:
                if date:
                    datetime.strptime(date, '%Y-%m-%d')
                    queryset = queryset.filter(check_in__date=date, is_deleted=False)
                if emp_id:
                    queryset = queryset.annotate(
                        full_name=Concat('employee__first_name', V(' '), 'employee__last_name',
                                         output_field=CharField())
                    ).filter(full_name__icontains=emp_id)
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = AttendanceSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = AttendanceSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AttendanceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeavesFilter(django_filters.FilterSet):
    status = filters.CharFilter(
        method='filter_leaves_status',
    )

    approved_by = filters.CharFilter(
        method='filter_approved_by',
    )

    employee_id = filters.CharFilter(
        method='filter_employee_id'
    )

    leave_type = filters.CharFilter(
        method='filter_leave_type',
    )

    class Meta:
        model = Leaves
        fields = ['employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date', 'status',
                  'approved_by']

    def filter_leaves_status(self, queryset, name, value):
        return queryset.filter(status=value)

    def filter_approved_by(self, queryset, name, value):
        return queryset.filter(approved_by__id=value)

    def filter_leave_type(self, queryset, name, value):
        return queryset.filter(leave_type=value)

    def filter_employee_id(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('employee__first_name', V(' '), 'employee__last_name')).
                filter(full_name__icontains=value))

    def filter_queryset(self, queryset):
        portal = self.request.query_params.get('portal')
        # Filtering logic for team lead
        user = self.request.user
        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = queryset.filter(employee__team_lead=user.id)
        if user.is_admin:
            pass
        else:
            employee = Employee.objects.get(id=user.id)
            if employee.is_team_lead:
                queryset = queryset.filter(employee__team_lead=user)
        return super().filter_queryset(queryset)


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavesPermission]
    queryset = Leaves.objects.all().order_by('-request_date')
    serializer_class = LeaveSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LeavesFilter
    pagination_class = CustomPageNumberPagination

    @staticmethod
    def remaining_leaves_per_month(user_id, request):
        employee = Employee.objects.filter(id=user_id)
        remaining_count = settings.MAX_LEAVES
        if employee:
            remaining_count = employee.get().total_leaves
        date = datetime.now()
        serializer_context = {
            'request': request,
        }
        current_month = date.month
        current_year = date.year
        leaves = Leaves.objects.filter(employee=user_id,
                                       request_date__month=current_month,
                                       request_date__year=current_year).exclude(status='REJECTED')
        if leaves:
            serializer = LeaveSerializer(leaves, many=True, context=serializer_context)
            data = serializer.data
            for remaining in data:
                days = remaining['number_of_days']
                remaining_count = remaining_count - int(days)
        return remaining_count

    @action(detail=False, url_name="get_leave", methods=['Get'])
    def get_leave(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        leaves = Leaves.objects.filter(employee=user.id).order_by('-request_date')
        count = self.remaining_leaves_per_month(user.id, request)
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(leaves, request)
        if leaves:
            serializer = LeaveSerializer(result_page, many=True, context=serializer_context)
            return paginator.get_paginated_response(({"data": serializer.data, "count": count}))
        return Response(({"count": count}), status=status.HTTP_200_OK)

    @action(detail=True, url_name="approve", methods=['PATCH'])
    def approve(self, request, pk):
        leave_list = ["SICK_LEAVE", "CASUAL_LEAVE", "MATERNITY_LEAVE", "PATERNITY_LEAVE", "MARRIAGE_LEAVE",
                      "EMERGENCY_LEAVE", "WORK_FROM_HOME"]
        leave = self.get_object()
        employee_name = f"{leave.employee.first_name} {leave.employee.last_name}"
        leave_type = leave.leave_type
        from_date = leave.from_date
        to_date = leave.to_date
        if 'status' in request.data:
            leave.status = request.data['status']
            if leave.status == 'PENDING':
                leave.approved_by = None
            else:
                leave.approved_by = request.user.employee
        if 'to_date' in request.data:
            leave.to_date = request.data['to_date']
        if 'from_date' in request.data:
            leave.from_date = request.data['from_date']
        leave.save()
        if (leave_type in leave_list) and leave.status == 'APPROVED':
            approved = leave.approved_by
            approved_by = f"{approved.first_name} {approved.last_name}"
            send_leave_request_message(employee_name, from_date, to_date, leave_type, "Approved", approved_by)
        return Response(
            status=status.HTTP_200_OK,
            data=LeaveSerializer(leave, context=self.get_serializer_context()).data)

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        if leave.status != 'PENDING':
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={f'Cannot delete Leave with status {leave.status}'})
        return super(LeavesViewSet, self).destroy(request, *args, **kwargs)


class AttendanceRequestFilter(django_filters.FilterSet):
    emp_id = filters.CharFilter(method='filter_employee_id')

    status = filters.CharFilter(
        method='filter_req_status',
    )

    approved_by = filters.CharFilter(
        method='filter_approved_by',
    )

    leave_type = filters.CharFilter(
        method='filter_check_type',
    )

    class Meta:
        model = AttendanceRequest
        fields = [
            "id",
            "employee",
            "check_type",
            "request_date",
            "attendance_date",
            "check_in_time",
            "check_out_time",
            "status",
            "reason",
            "approved_by",
        ]

    def filter_req_status(self, queryset, name, value):
        return queryset.filter(status=value)

    def filter_approved_by(self, queryset, name, value):
        return queryset.filter(approved_by__id=value)

    def filter_check_type(self, queryset, name, value):
        return queryset.filter(check_type=value)


    def filter_employee_id(self, queryset, name, value):
        return queryset.filter(employee__id=value)

    def filter_queryset(self, queryset):
        portal = self.request.query_params.get('portal')
        # Filtering logic for team lead
        user = self.request.user
        if (user.is_admin or user.employee.is_team_lead) and portal == 'team_lead':
            queryset = queryset.filter(employee__team_lead=user.id)
        if user.is_admin:
            pass
        else:
            employee = Employee.objects.get(id=user.id)
            if employee.is_team_lead:
                queryset = queryset.filter(employee__team_lead=user)
        return super().filter_queryset(queryset)


class AttendanceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRequestSerializer
    permission_classes = [IsAuthenticated, AttendanceRequestPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttendanceRequestFilter

    def get_queryset(self):
        return AttendanceRequest.objects.all().order_by('-request_date')

    @action(detail=False, methods=['post'], url_path='create')
    def create_attendance_request(self, request):
        user = request.user
        data = request.data.copy()
        data['employee'] = user.employee.id

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Attendance request submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='approve_req')
    def approve_req(self, request, pk=None):
        correction_request = self.get_object()

        status_value = request.data.get('status')
        print(status_value)
        if status_value not in ['APPROVED', 'REJECTED', 'PENDING']:
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        attendance_date = request.data.get('attendance_date', correction_request.attendance_date)
        if isinstance(attendance_date, str):
            try:
                attendance_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"detail": "Invalid attendance_date format. Use YYYY-MM-DD."},
                                status=status.HTTP_400_BAD_REQUEST)

        check_in_time = request.data.get('check_in_time',
                                         correction_request.check_in_time)
        check_out_time = request.data.get('check_out_time',
                                          correction_request.check_out_time)

        TIME_FORMAT = '%H:%M:%S'
        if check_in_time:
            if isinstance(check_in_time, str):
                try:
                    check_in_time = datetime.strptime(check_in_time, TIME_FORMAT).time()
                except ValueError:
                    return Response({"detail": "Invalid check-in time format. Use HH:MM:SS."},
                                    status=status.HTTP_400_BAD_REQUEST)
        elif check_in_time is None:
            check_in_time = None

        if check_out_time:
            if isinstance(check_out_time, str):
                try:
                    check_out_time = datetime.strptime(check_out_time, TIME_FORMAT).time()
                except ValueError:
                    return Response({"detail": "Invalid check-out time format. Use HH:MM:SS."},
                                    status=status.HTTP_400_BAD_REQUEST)
        elif check_out_time is None:
            check_out_time = None

            # Apply updates
        correction_request.check_type = request.data.get('check_type', correction_request.check_type)
        correction_request.attendance_date = attendance_date
        correction_request.check_in_time = check_in_time
        correction_request.check_out_time = check_out_time
        correction_request.status = status_value
        correction_request.approved_by = request.user.employee
        correction_request.save()

        # If APPROVED, update or create attendance record
        if status_value == 'APPROVED':
            employee = correction_request.employee
            check_type = correction_request.check_type

            if check_type == 'CHECK_IN' and not check_in_time:
                return Response({"detail": "Missing check-in time."}, status=status.HTTP_400_BAD_REQUEST)
            if check_type == 'CHECK_OUT' and not check_out_time:
                return Response({"detail": "Missing check-out time."}, status=status.HTTP_400_BAD_REQUEST)
            if check_type == 'CHECK_IN_CHECK_OUT' and (not check_in_time or not check_out_time):
                return Response({"detail": "Both check-in and check-out times are required."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Make aware datetime objects
            check_in_dt = make_aware(
                datetime.combine(attendance_date, check_in_time)) if check_in_time else None
            check_out_dt = make_aware(
                datetime.combine(attendance_date, check_out_time)) if check_out_time else None

            total_time = None
            if check_in_dt and check_out_dt:
                total_time = check_out_dt - check_in_dt if check_out_dt > check_in_dt else timedelta()

            # Update or create attendance
            attendance = Attendance.objects.filter(employee=employee, check_in__date=attendance_date).first()
            if attendance:
                if check_type in ['CHECK_IN', 'CHECK_IN_CHECK_OUT']:
                    attendance.check_in = check_in_dt
                if check_type in ['CHECK_OUT', 'CHECK_IN_CHECK_OUT']:
                    attendance.check_out = check_out_dt
                if check_in_dt and check_out_dt:
                    attendance.total_time = total_time
                attendance.save()
            else:
                Attendance.objects.create(
                    employee=employee,
                    check_in=check_in_dt if check_type in ['CHECK_IN', 'CHECK_IN_CHECK_OUT'] else None,
                    check_out=check_out_dt if check_type in ['CHECK_OUT', 'CHECK_IN_CHECK_OUT'] else None,
                    total_time=total_time if check_in_dt and check_out_dt else None,
                    status='ATTENDANCE_REQUEST'
                )
        serializer = self.get_serializer(correction_request)
        return Response({"success": f"Request {status_value.lower()}.","data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        att_req = self.get_object()
        if att_req.status != 'PENDING':
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={f'Cannot delete Leave with status {att_req.status}'})
        return super(AttendanceRequestViewSet, self).destroy(request, *args, **kwargs)
