from django.http import JsonResponse
from rest_framework.response import Response
from attendance.serializers import AttendanceSerializer, LeaveSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from attendance.models import Attendance, Leaves
from datetime import datetime


class AttendanceViewSet(viewsets.ModelViewSet):
    view_permissions = {
        'retrieve': {'admin': True},
        'create': {'employee': True, 'admin': True},
        'list': {'admin': True},
        'update': {'employee': True, 'admin': True},
        'partial_update': {'employee': True, 'admin': True},
    }
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        att_type = request.data['action']
        user = request.user
        record = Attendance.objects.filter(employee_id=user.id, check_in__contains=datetime.now().date())
        if att_type == "check-in":
            if not record:
                current_date = datetime.now()
                check_in = Attendance.objects.create(
                    employee_id=user.id,
                    check_in=current_date,
                    status="ON_TIME"
                )
                return JsonResponse({"success": f"employee {att_type} successfully"}, status=status.HTTP_201_CREATED)
            return JsonResponse({"error": f"Employee {att_type} already today"}, status=status.HTTP_208_ALREADY_REPORTED)
        return JsonResponse({"error": "Please enter valid action"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def partial_update(self, request, *args, **kwargs):
        att_type = request.data['action']
        user = request.user
        checked_in = Attendance.objects.filter(employee_id=user.id, check_in__contains=datetime.now().date())
        if att_type == "check-out":
            if checked_in.exists():
                checked_out = Attendance.objects.filter(employee_id=user.id,
                                                        check_out__contains=datetime.now().date())
                if not checked_out:
                    current_date = datetime.now()
                    check_out = Attendance.objects.update(
                        check_out=current_date,
                    )
                    return JsonResponse({"success": f"Employee has {att_type} successfully"}, status=status.HTTP_200_OK)
                return JsonResponse({"error": f"Employee has already {att_type}"}, status=status.HTTP_208_ALREADY_REPORTED)
            return JsonResponse({"error": f"Employee did not check in today"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return JsonResponse({"error": f"Please enter valid action"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        attendance = self.get_object()
        attendance.is_deleted = True
        attendance.save()
        return Response(data=f'Attendance with id {attendance.id} deleted successfully')


class LeavesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Leaves.objects.all()
    serializer_class = LeaveSerializer

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        leave.is_deleted = True
        leave.save()
        return Response(data=f'Attendance with id {leave.id} deleted successfully')