from rest_framework import serializers

from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "status"]

    def to_representation(self, instance):
        ret = super(AttendanceSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.first_name + " " + instance.employee.last_name)
        ret['date_time_check_in'] = str(str(instance.check_in.day) + "-" + str(instance.check_in.month) + "-"
                                        + str(instance.check_in.year) + " / " + str(instance.check_in.hour + 5) + ":" +
                                        str(instance.check_in.minute) + ":" + str(instance.check_in.second))
        if instance.check_out is None or instance.check_out is False:
            pass
        else:
            ret['date_time_check_out'] = str(str(instance.check_out.day) + "-" + str(instance.check_out.month) + "-"
                                             + str(instance.check_out.year) + " / " + str(
                                                instance.check_out.hour + 5) + ":" +
                                             str(instance.check_out.minute) + ":" + str(instance.check_out.second))
        return ret


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date']
