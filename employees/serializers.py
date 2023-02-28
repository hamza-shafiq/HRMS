from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from employees.models import Department, Employee
from user.tasks import generate_and_send_employee_credentials


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
    employee_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = Employee
        fields = ['id', 'employee_name', 'assets', 'username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'national_id_number', 'emergency_contact_number', 'gender', 'department',
                  'designation', 'bank', 'account_number', 'profile_pic', 'joining_date', 'employee_status',
                  'is_verified', 'is_active']

    def to_representation(self, instance):
        ret = super(EmployeeSerializer, self).to_representation(instance)
        del ret['department']
        ret['department_id'] = str(instance.department_id)
        ret['department'] = str(instance.department)
        return ret

    def validate_password(self, value):
        if value:
            email_body = 'Hi ' + self.initial_data['username'] + '!\n' + \
                         ' Here is your password for HRMS Portal \n' + value
            data = {'email_body': email_body, 'to_email': self.initial_data['email'],
                    'email_subject': 'Password'}
            generate_and_send_employee_credentials(data)
            return make_password(value)
        return value
