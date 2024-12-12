from rest_framework import serializers

from user import manager
from .models import Projects

class ProjectsSerializer(serializers.ModelSerializer):
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

        if instance.team_members.exists():
            ret['team_members'] = [
                    {
                        'team_member_id': str(member.id),
                        'team_member_name': f"{member.employee.first_name} {member.employee.last_name}"
                    }
                    for member in instance.team_members.all()
            ]
        if instance.account_manager:
            ret['account_manager'] = [
                {
                    'account_manager_id': str(instance.account_manager.id),
                    'account_manager_name': f"{instance.account_manager.first_name} {instance.account_manager.last_name}"

                }
            ]


        return ret