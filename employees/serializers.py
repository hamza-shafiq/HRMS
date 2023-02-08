from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from employees.models import Department, Employee


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='employees-detail'
    )

    class Meta:
        model = Department
        fields = ["url", "id", "department_name", "description", "employees"]


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    assets = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assigned-asset-detail'
    )
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'assets', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                  'national_id_number', 'emergency_contact_number', 'gender', 'department', 'designation', 'bank',
                  'account_number', 'profile_pic', 'joining_date', 'employee_status', 'is_verified', 'is_active']

    def to_representation(self, instance):
        ret = super(EmployeeSerializer, self).to_representation(instance)
        del ret['department']
        ret['department_id'] = str(instance.department_id)
        ret['department'] = str(instance.department)
        return ret

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value
