from datetime import datetime

from rest_framework import serializers

from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "status"]

    def to_representation(self, instance):
        ret = super(AttendanceSerializer, self).to_representation(instance)
        ret['employee_name'] = str(str(instance.employee.first_name).capitalize() + " " +
                                   str(instance.employee.last_name).capitalize())
        dt = datetime.strptime(str(instance.check_in), '%Y-%m-%d %H:%M:%S.%f+00:00')
        ret['time_check_in'] = str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" + str(dt.second).zfill(2)
        ret['check_in_date'] = dt.date()

        ret['check in time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)

        if instance.check_out is None or instance.check_out is False:
            pass
        else:
            dt = datetime.strptime(str(instance.check_out), '%Y-%m-%d %H:%M:%S.%f+00:00')
            ret['time_check_out'] = str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" + str(
                dt.second).zfill(2)

            ret['check_out_date'] = dt.date()

            ret['check out time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)
        return ret


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date', 'status']

    @staticmethod
    def difference_date(from_date, to_date):
        date1 = datetime.strptime(from_date, '%Y-%m-%d')
        date2 = datetime.strptime(to_date, '%Y-%m-%d')

        delta = date2 - date1
        return delta.days

    def to_representation(self, instance):
        ret = super(LeaveSerializer, self).to_representation(instance)

        ret['employee_name'] = str(instance.employee.get_full_name)
        ret.pop('request_date')

        ret['request_date'] = str(str(instance.request_date.day).zfill(2) + "-" +
                                  str(instance.request_date.month).zfill(2) + "-" +
                                  str(instance.request_date.year).zfill(2))

        difference = self.difference_date(str(instance.from_date), str(instance.to_date))

        ret['number_of_days'] = str(difference + 1)

        return ret
