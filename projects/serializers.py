from rest_framework import serializers
from projects.models import Projects, Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'employee', 'project', 'start_date', 'end_date', 'engagement_type', 'employee_name']

    def get_employee_name(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return None

class ProjectsSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(ProjectsSerializer, self).to_representation(instance)
        if instance.team_lead:
            ret['team_lead'] = {
                'team_lead_id': str(instance.team_lead.id),
                'team_lead_name': instance.team_lead.first_name + ' ' + instance.team_lead.last_name
            }


        if instance.team_lead:
            ret['team_members'] = [
                {
                    'id': assignment.id,
                    'employee_id': str(assignment.employee.id),
                    'team_member_name': f"{assignment.employee.first_name} {assignment.employee.last_name}",
                    'start_date': assignment.start_date,
                    'end_date': assignment.end_date,
                    'engagement_type': assignment.engagement_type
                }
                for assignment in instance.assignments.all()
            ]

        if instance.account_manager:
            ret['account_manager'] = [
                {
                    'account_manager_id': str(instance.account_manager.id),
                    'account_manager_name': f"{instance.account_manager.first_name} {instance.account_manager.last_name}"
                }
            ]

        return ret