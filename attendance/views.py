from datetime import datetime

import django_filters
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance, Leaves
from attendance.permissions import AttendancePermission, LeavesPermission
from attendance.serializers import AttendanceSerializer, LeaveSerializer
from employees.models import Employee
from hrms.pagination import CustomPageNumberPagination


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
        queryset = Attendance.objects.all().order_by('-check_in')
        if date or emp_id:
            try:
                if date:
                    datetime.strptime(date, '%Y-%m-%d')
                    record = queryset.filter(check_in__date=date, is_deleted=False)
                if emp_id:
                    record = record.annotate(
                        full_name=Concat('employee__first_name', V(' '), 'employee__last_name',
                                         output_field=CharField())
                    ).filter(full_name__icontains=emp_id)
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
            page = self.paginate_queryset(record)
            if page is not None:
                serializer = AttendanceSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = AttendanceSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Attendance.objects.all().order_by('-check_in')

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

    class Meta:
        model = Leaves
        fields = ['employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date', 'status',
                  'approved_by']

    def filter_leaves_status(self, queryset, name, value):
        return queryset.filter(status=value)

    def filter_approved_by(self, queryset, name, value):
        return queryset.filter(approved_by__id=value)

    def filter_employee_id(self, queryset, name, value):
        return (queryset.annotate(full_name=Concat('employee__first_name', V(' '), 'employee__last_name')).
                filter(full_name__icontains=value))


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavesPermission]
    queryset = Leaves.objects.all().order_by('-created')
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
        leaves = Leaves.objects.filter(employee=user.id).order_by('-created')
        count = self.remaining_leaves_per_month(user.id, request)
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(leaves, request)
        if leaves:
            serializer = LeaveSerializer(result_page, many=True, context=serializer_context)
            return paginator.get_paginated_response(({"data": serializer.data, "count": count}))
        return Response(({"count": count}), status=status.HTTP_200_OK)

    @action(detail=True, url_name="approve", methods=['PATCH'])
    def approve(self, request, pk):
        leave = self.get_object()
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
        return Response(
            status=status.HTTP_200_OK,
            data=LeaveSerializer(leave, context=self.get_serializer_context()).data)

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        if leave.status != 'PENDING':
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={f'Cannot delete Leave with status {leave.status}'})
        return super(LeavesViewSet, self).destroy(request, *args, **kwargs)
