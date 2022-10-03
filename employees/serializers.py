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
    assets = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assigned-asset-detail'
    )

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    # TODO when creating an employee add to the employee Group Model to limit the access
