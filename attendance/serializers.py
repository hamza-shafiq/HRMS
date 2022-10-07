from rest_framework import serializers
from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "status"]


class LeaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date']
