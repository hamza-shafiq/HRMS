from django.http import JsonResponse
from rest_framework.response import Response
from attendance.permissions import AttendancePermission, LeavePermission
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

        if action_type == "check-in":
            if not record:
                Attendance.objects.create(employee_id=user.id, check_in=current_datetime, status="ON_TIME")
                return JsonResponse({"success": f"employee checked-in successfully!"}, status=status.HTTP_201_CREATED)

            return JsonResponse({"error": f"Employee already checked-in today!"}, status=status.HTTP_208_ALREADY_REPORTED)

        elif action_type == "check-out":
            if not record:
                return JsonResponse({"error": f"Employee did not check-in today!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            record.update(check_out=current_datetime)
            return JsonResponse({"success": f"employee checked-out successfully!"}, status=status.HTTP_200_OK)

        return JsonResponse({"error": "Please enter valid action (check-in/check-out)"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        attendance = self.get_object()
        attendance.is_deleted = True
        attendance.save()
        return Response(data=f'Attendance with id {attendance.id} deleted successfully')


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LeavePermission]
    queryset = Leaves.objects.all()
    serializer_class = LeaveSerializer

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        leave.is_deleted = True
        leave.save()
        return Response(data=f'Attendance with id {leave.id} deleted successfully')
