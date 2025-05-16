from datetime import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from attendance.models import Attendance, Leaves
from attendance.utils import send_leave_request_message
from .models import AttendanceRequest

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "check_in", "check_out", "total_time", "status"]

    def to_representation(self, instance):
        ret = super(AttendanceSerializer, self).to_representation(instance)
        ret['employee_name'] = str(str(instance.employee.first_name).capitalize() + " " +
                                   str(instance.employee.last_name).capitalize())
        dt = datetime.strptime(str(instance.check_in), settings.DATETIME_FORMAT)
        ret['time_check_in'] = (str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" +
                                str(dt.second).zfill(2))
        ret['check_in_date'] = dt.date()

        ret['check in time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)

        if instance.check_out is None or instance.check_out is False:
            pass
        else:
            dt = datetime.strptime(str(instance.check_out), settings.DATETIME_FORMAT)
            ret['time_check_out'] = str(dt.hour + 5).zfill(2) + ":" + str(dt.minute).zfill(2) + ":" + str(
                dt.second).zfill(2)

            ret['check_out_date'] = dt.date()

            ret['check out time'] = str(dt.hour + 5).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)
            ret['total_time'] = str(str(instance.total_time))
        return ret


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'employee', 'leave_type', 'reason', 'request_date', 'from_date', 'to_date', 'status',
                  'approved_by']

    def create(self, validated_data):
        employee = validated_data['employee']
        name = employee.first_name + " " + employee.last_name
        leave_type = validated_data['leave_type']
        start_date = validated_data['from_date']
        end_date = validated_data['to_date']
        status = "Pending"
        team_lead = employee.team_lead
        leave_list = ["SICK_LEAVE", "CASUAL_LEAVE", "MATERNITY_LEAVE", "PATERNITY_LEAVE", "MARRIAGE_LEAVE",
                      "EMERGENCY_LEAVE", "WORK_FROM_HOME"]
        if team_lead is None:
            team_lead_name = "-"
        else:
            team_lead_name = team_lead.first_name + " " + team_lead.last_name
        if leave_type in leave_list:
            send_leave_request_message(name, start_date, end_date, leave_type, status, team_lead_name)
        return Leaves.objects.create(**validated_data)

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
        return ret


class AttendanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRequest
        fields = '__all__'
        read_only_fields = ['employee', 'status', 'approved_by', 'request_date']

    def validate(self, data):
        check_type = data.get('check_type')
        if check_type == 'CHECK_IN' and not data.get('check_in_time'):
            raise serializers.ValidationError("check-in time is required for CHECK_IN.")
        if check_type == 'CHECK_OUT' and not data.get('check_out_time'):
            raise serializers.ValidationError("check-out time is required for CHECK_OUT.")
        if check_type == 'CHECK_IN_CHECK_OUT' and (
                not data.get('check_in_time') or not data.get('check_out_time')):
            raise serializers.ValidationError("Both check-in and check-out times are required for BOTH.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["employee"] = request.user.employee
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super(AttendanceRequestSerializer, self).to_representation(instance)
        ret['employee_name'] = str(instance.employee.get_full_name)
        if instance.approved_by:
            ret['approved_by'] = {
                'approved_by_id': str(instance.approved_by.id),
                'approved_by_name': instance.approved_by.get_full_name
            }
        return ret

