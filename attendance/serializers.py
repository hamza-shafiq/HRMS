from rest_framework import serializers

from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "status"]

    def to_representation(self, instance):
        ret = super(AttendanceSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.first_name + " " + instance.employee.last_name)
        ret['date_time_check_in'] = str(str(instance.check_in.day).zfill(2) + "-"
                                        + str(instance.check_in.month).zfill(2) + "-"
                                        + str(instance.check_in.year).zfill(2) + " / " +
                                        str(instance.check_in.hour + 5).zfill(2) + ":" +
                                        str(instance.check_in.minute).zfill(2) +
                                        ":" + str(instance.check_in.second).zfill(2))

        ret['check_in_date'] = str(str(instance.check_in.day).zfill(2) + "-" + str(instance.check_in.month).zfill(2)
                                   + "-" + str(instance.check_in.year))

        ret['check_in_time'] = str(str(instance.check_in.hour + 5).zfill(2) +
                                   str(instance.check_in.minute).zfill(2) + str(instance.check_in.second).zfill(2))

        if instance.check_out is None or instance.check_out is False:
            pass
        else:
            ret['date_time_check_out'] = str(str(instance.check_out.day).zfill(2) + "-" +
                                             str(instance.check_out.month).zfill(2) + "-"
                                             + str(instance.check_out.year).zfill(2) + " / " + str(
                                                instance.check_out.hour + 5).zfill(2) + ":" +
                                             str(instance.check_out.minute).zfill(2) +
                                             ":" + str(instance.check_out.second).zfill(2))

            ret['check_out_date'] = str(str(instance.check_out.day) + "-" + str(instance.check_out.month) + "-"
                                        + str(instance.check_out.year))

            ret['check_out_time'] = str(str(instance.check_out.hour + 5).zfill(2) +
                                        str(instance.check_out.minute).zfill(2) +
                                        str(instance.check_out.second).zfill(2))
        return ret


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date']
