from datetime import datetime

from django.conf import settings
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
        # Check-in time
        dt_check_in = instance.check_in
        ret['time_check_in'] = dt_check_in.strftime('%H:%M:%S')
        ret['check_in_date'] = dt_check_in.date()
        ret['check_in_time'] = dt_check_in.strftime('%H%M%S')

        # Check-out time
        if instance.check_out is not None and instance.check_out is not False:
            dt_check_out = instance.check_out
            ret['time_check_out'] = dt_check_out.strftime('%H:%M:%S')
            ret['check_out_date'] = dt_check_out.date()
            ret['check_out_time'] = dt_check_out.strftime('%H%M%S')

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
        ret['extra_leaves'] = str(instance.employee.extra_leaves)
        return ret
