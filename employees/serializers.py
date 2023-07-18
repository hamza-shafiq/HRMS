from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import User

from attendance.serializers import LeaveSerializer
from employees.models import Department, Employee
from user.tasks import send_email
from collections import defaultdict


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
    username = serializers.CharField(required=True, write_only=True)
    employee_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = Employee
        fields = ['id', 'employee_name', 'assets', 'username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'national_id_number', 'emergency_contact_number', 'gender', 'department',
                  'designation', 'bank', 'account_number', 'profile_pic', 'joining_date', 'employee_status',
                  'is_verified', 'is_active']

    def create(self, validated_data):
        email = validated_data.get('email')

        # Check if there is a soft-deleted user with the same email
        try:
            user = User.all_objects.get(email=email, is_deleted=True)
            if user:
                user.reactivate_user()
                user = Employee.objects.get(email=email)
                return user
        except User.DoesNotExist:
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
        return ret

    @staticmethod
    def get_leaves_dict(leave):
        leaves = defaultdict(int)
        for leave_data in leave.data:
            leave_type = leave_data['leave_type']
            number_of_days = leave_data['number_of_days']
            leaves['total_leaves'] = "20"
            leaves['remaining_leaves'] = leave_data['remaining_leaves']
            leaves[leave_type] += int(number_of_days)
        return leaves

    def validate_password(self, value):
        if value:
            email_body = 'Hi ' + self.initial_data['username'] + '!\n' + \
                         ' Here is your password for HRMS Portal \n' + value
            data = {'email_body': email_body, 'to_email': self.initial_data['email'],
                    'email_subject': 'Password'}
            # generate_and_send_employee_credentials(data)
            send_email.delay(data)
            return make_password(value)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
