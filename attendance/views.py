from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance, Leaves
from attendance.permissions import AttendancePermission, LeavesPermission
from attendance.serializers import AttendanceSerializer, LeaveSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AttendancePermission]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, url_name="get-attendance", methods=['Get'])
    def get_attendance(self, request):
        user = request.user
        serializer_context = {
            'request': request,
        }
        attendance = Attendance.objects.filter(employee=user.id).order_by('-check_in__date')
        if attendance:
            serializer = AttendanceSerializer(attendance, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'You did not check-in today'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path="mark-attendance", methods=['post'])
    def mark_attendance(self, request):
        action_type = request.data.get("action", None)
        user = request.user
        current_datetime = datetime.now()
        record = Attendance.objects.filter(employee_id=user.id, check_in__contains=current_datetime.date()).first()
        if hasattr(user, 'employee'):
            if action_type == "check-in":
                if not record:
                    Attendance.objects.create(employee_id=user.id, check_in=current_datetime, status="ON_TIME")
                    return JsonResponse({"success": "Employee checked-in successfully!"},
                                        status=status.HTTP_201_CREATED)

                return JsonResponse({"detail": "Employee already checked-in today!"},
                                    status=status.HTTP_208_ALREADY_REPORTED)

            elif action_type == "check-out":
                if not record:
                    return JsonResponse({"detail": "Employee did not check-in today!"},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

                record.check_out = current_datetime
                record.save()
                return JsonResponse({"success": "Employee checked-out successfully!"}, status=status.HTTP_200_OK)

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
        if date or emp_id:
            try:
                if date:
                    datetime.strptime(date, '%Y-%m-%d')
                    record = Attendance.objects.filter(check_in__date=date,
                                                       is_deleted=False).order_by('-check_in__date')
                if emp_id:
                    if date:
                        record = record.filter(employee_id=emp_id).order_by('-check_in__date')
                    else:
                        record = Attendance.objects.filter(employee_id=emp_id,
                                                           is_deleted=False).order_by('-check_in__date')
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = AttendanceSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Attendance.objects.all().order_by('-check_in__date')
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavesPermission]
    queryset = Leaves.objects.all().order_by('-created')
    serializer_class = LeaveSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['employee_id', "status"]

    @staticmethod
    def remaining_leaves_per_month(user_id, request):
        remaining_count = settings.MAX_LEAVES
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
        if leaves:
            serializer = LeaveSerializer(leaves, many=True, context=serializer_context)
            return Response(({"data": serializer.data, "count": count}), status=status.HTTP_200_OK)
        return Response(({"count": count}), status=status.HTTP_200_OK)

