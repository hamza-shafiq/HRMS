from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from employees.models import Employee, Department


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='employees-detail'
    )

    class Meta:
        model = Department
        fields = '__all__'


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

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
