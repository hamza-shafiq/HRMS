from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
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
        attendance = Attendance.objects.filter(employee=user.id)
        if attendance:
            serializer = AttendanceSerializer(attendance, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'You did not check-in today'}, status=status.HTTP_404_NOT_FOUND)

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
        return JsonResponse({'detail': 'You did not check-in today'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        date = self.request.query_params.get('date')
        # emp_id = self.request.query_params.get('employee_id')
        # if date or emp_id:  # change operator for filtering for date only
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
                record = Attendance.objects.filter(check_in__date=date, is_deleted=False)
            except ValidationError:
                return JsonResponse({'detail': 'Invalid employee id'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = AttendanceSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Attendance.objects.all()
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavesPermission]
    queryset = Leaves.objects.all()
    serializer_class = LeaveSerializer
