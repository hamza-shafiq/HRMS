from django.http import JsonResponse
from rest_framework.response import Response
from attendance.permissions import AttendancePermission, LeavesPermission
from attendance.serializers import AttendanceSerializer, LeaveSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from attendance.models import Attendance, Leaves
from datetime import datetime
from rest_framework.decorators import action


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AttendancePermission]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, url_path="mark-attendance")
    def mark_attendance(self, request):
        action_type = request.data.get("action", None)
        user = request.user
        current_datetime = datetime.now()
        record = Attendance.objects.filter(employee_id=user.id, check_in__contains=current_datetime.date()).first()

        if hasattr(user, 'employee'):
            if action_type == "check-in":
                if not record:
                    Attendance.objects.create(employee_id=user.id, check_in=current_datetime, status="ON_TIME")
                    return JsonResponse({"success": "employee checked-in successfully!"},
                                        status=status.HTTP_201_CREATED)

                return JsonResponse({"error": "Employee already checked-in today!"},
                                    status=status.HTTP_208_ALREADY_REPORTED)

            elif action_type == "check-out":
                if not record:
                    return JsonResponse({"error": "Employee did not check-in today!"},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

                record.check_out = current_datetime
                record.save()
                return JsonResponse({"success": "employee checked-out successfully!"}, status=status.HTTP_200_OK)

            return JsonResponse({"error": "Please enter valid action (check-in/check-out)"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse({"error": "Only employee can mark the attendance"},
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        attendance = self.get_object()
        attendance.is_deleted = True
        attendance.save()
        return Response(data=f'Attendance with id {attendance.id} deleted successfully')


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavesPermission]
    queryset = Leaves.objects.all()
    serializer_class = LeaveSerializer

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        leave.is_deleted = True
        leave.save()
        return Response(data=f'Attendance with id {leave.id} deleted successfully')
