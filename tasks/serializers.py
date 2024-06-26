from rest_framework import serializers

from tasks.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'assigned_by', 'employee', 'deadline', 'created_on', 'status']

    def to_representation(self, instance):
        ret = super(TasksSerializer, self).to_representation(instance)
        if instance.assigned_by:
            ret['assigned_by'] = {
                'assigned_by_id': str(instance.assigned_by.id),
                'assigned_by_name': instance.assigned_by.get_full_name
            }

        if instance.employee:
            ret['employee'] = {
                'employee_id': str(instance.employee.id),
                'employee_name': instance.employee.get_full_name
            }

        return ret
