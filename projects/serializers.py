from rest_framework import serializers
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
                        'team_member_name': f"{member.first_name} {member.last_name}"
                    }
                    for member in instance.team_members.all()
            ]

        return ret