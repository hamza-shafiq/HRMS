from rest_framework import serializers
from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()

    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leaves
        fields = '__all__'