from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from attendance.models import Attendance, Leaves


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "status"]

    def to_representation(self, instance):
        ret = super(AttendanceSerializer, self).to_representation(instance)
        ret['employee_name'] = str(str(instance.employee.first_name).capitalize() + " " +
                                   str(instance.employee.last_name).capitalize())
        dt = datetime.strptime(str(instance.check_in), '%Y-%m-%d %H:%M:%S%z')
        ret['time_check_in'] = str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" + str(dt.second).zfill(2)
        ret['check_in_date'] = dt.date()

        ret['check in time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)

        if instance.check_out is None or instance.check_out is False:
            pass
        else:
            dt = datetime.strptime(str(instance.check_out), '%Y-%m-%d %H:%M:%S%z')
            ret['time_check_out'] = str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" + str(
                dt.second).zfill(2)

            ret['check_out_date'] = dt.date()

            ret['check out time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)
        return ret


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date', 'status',
                  'approved_by']

    def update(self, instance, validated_data):
        if instance.status != 'PENDING':
            raise ValidationError(f"Cannot update Leave Information after {instance.status} status")
        valid_keys_for_update = ['from_date', 'to_date', 'reason', 'leave_type', 'request_date']
        invalid_keys = set(validated_data.keys()) - set(valid_keys_for_update)
        if invalid_keys:
            raise ValidationError(
                "Cannot update leave information, valid keys are: {}.".format(','.join(valid_keys_for_update))
            )
        return super().update(instance, validated_data)

    @staticmethod
    def difference_date(from_date, to_date):
        date1 = datetime.strptime(from_date, '%Y-%m-%d')
        date2 = datetime.strptime(to_date, '%Y-%m-%d')

        delta = date2 - date1
        return delta.days

    def to_representation(self, instance):
        ret = super(LeaveSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.get_full_name)
        if instance.approved_by:
            ret['approved_by'] = {
                'approved_by_id': str(instance.approved_by.id),
                'approved_by_name': instance.approved_by.get_full_name
            }
        difference = self.difference_date(str(instance.from_date), str(instance.to_date))
        ret['number_of_days'] = str(difference + 1)
        ret['remaining_leaves'] = str(instance.employee.remaining_leaves)
        return ret
