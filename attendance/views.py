from django.http import JsonResponse
from rest_framework.response import Response
from attendance.serializers import AttendanceSerializer, LeaveSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from attendance.models import Attendance, Leaves
from datetime import datetime
from rest_framework.decorators import action
import logging
logger = logging.getLogger(__name__)
# logger.setLevel('DEBUG')


class AttendanceViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True, 'employee': True},
        'create': {'employee': True, 'admin': True},
        'list': {'admin': True, 'employee': True},
        'update': {'employee': True, 'admin': True},
        'partial_update': {'employee': True, 'admin': True},
    }
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, url_path="mark-attendance")
    def mark_attendance(self, request):
        action_type = request.data.get("action", None)
        user = request.user
        current_datetime = datetime.now()
        record = Attendance.objects.filter(employee_id=user.id, check_in__contains=current_datetime.date()).first()

        if action_type == "check-in":
            if not record:
                Attendance.objects.create(employee_id=user.id, check_in=current_datetime, status="ON_TIME")
                logger.info(f'Employee with id {user.id} checked-in successfully')
                return JsonResponse({"success": f"employee checked-in successfully!"},
                                    status=status.HTTP_201_CREATED)
            logger.info(f'Employee with id {user.id} already checked-in today')
            return JsonResponse({"error": f"Employee already checked-in today!"},
                                status=status.HTTP_208_ALREADY_REPORTED)

        elif action_type == "check-out":
            if not record:
                logger.info(f'Employee with id {user.id} did not check-in today')
                return JsonResponse({"error": f"Employee did not check-in today!"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

            record.check_out = current_datetime
            record.save()
            logger.info(f'Employee with id {user.id}checked-out successfully')
            return JsonResponse({"success": f"employee checked-out successfully!"}, status=status.HTTP_200_OK)

        logger.info(f'Please enter valid action (check-in/check-out) for employee with id {user.id}')
        return JsonResponse({"error": "Please enter valid action (check-in/check-out)"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        attendance = self.get_object()
        attendance.is_deleted = True
        attendance.save()
        logger.info(f'Attendance with id {attendance.id} deleted successfully')
        return Response(data=f'Attendance with id {attendance.id} deleted successfully')


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Leaves.objects.all()
    serializer_class = LeaveSerializer

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        leave.is_deleted = True
        leave.save()
        logger.log(f'Leave with id {leave.id} deleted successfully')
        return Response(data=f'Leave with id {leave.id} deleted successfully')
