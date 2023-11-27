from collections import defaultdict

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from attendance.serializers import LeaveSerializer
from employees.models import Department, Employee
from user.models import User
from user.tasks import send_email


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='employees-detail'
    )

    class Meta:
        model = Department
        fields = ["url", "id", "department_name", "description", "employees"]

    def to_representation(self, instance):
        ret = super(DepartmentSerializer, self).to_representation(instance)
        ret['employees_count'] = str(instance.employees.filter(employee_status='WORKING', is_active=True).count())
        return ret


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    assets = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assigned-asset-detail'
    )
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(required=True)
    employee_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = Employee
        fields = ['id', 'employee_name', 'assets', 'username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'national_id_number', 'emergency_contact_number', 'gender', 'department',
                  'designation', 'bank', 'account_number', 'profile_pic', 'joining_date', 'employee_status',
                  'is_verified', 'is_active', 'total_leaves', 'remaining_leaves']

    def create(self, validated_data):
        email = validated_data.get('email')

        # Check if there is a soft-deleted user with the same email
        try:
            user = User.all_objects.get(email=email, is_deleted=True)
            if user:
                user.reactivate_user(password=validated_data.get('password'))
                user = Employee.objects.get(email=email)
                return user
        except User.DoesNotExist:
            total_leaves = validated_data.get('total_leaves')
            if total_leaves:
                validated_data['remaining_leaves'] = total_leaves
            return Employee.objects.create(**validated_data)

    def to_representation(self, instance):
        leaves = LeaveSerializer(instance.leaves.filter(status='APPROVED'), many=True)
        leave_dict = self.get_leaves_dict(leaves)
        if not leave_dict:
            leave_dict = {}

        ret = super(EmployeeSerializer, self).to_representation(instance)
        del ret['department']
        ret['department_id'] = str(instance.department_id)
        ret['department'] = str(instance.department)
        ret['leaves'] = leave_dict
        leave_dict['total_leaves'] = instance.total_leaves
        leave_dict['remaining_leaves'] = instance.remaining_leaves
        if instance.remaining_leaves > instance.total_leaves:
            leave_dict['remaining_leaves'] = instance.total_leaves
        return ret

    @staticmethod
    def get_leaves_dict(leave):
        leaves = defaultdict(int)
        for leave_data in leave.data:
            leave_type = leave_data['leave_type']
            number_of_days = leave_data['number_of_days']
            leaves[leave_type] += int(number_of_days)
        return leaves

    def validate_password(self, value):
        if value:
            email_body = 'Hi ' + self.initial_data['username'] + '!\n' + \
                         ' Here is your password for HRMS Portal \n' + value
            data = {'email_body': email_body, 'to_email': self.initial_data['email'],
                    'email_subject': 'Password'}
            send_email.delay(data)
            return make_password(value)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
