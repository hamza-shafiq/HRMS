from django.core.exceptions import ValidationError
from rest_framework import serializers
from policies.models import Policies


class PolicySerializer(serializers.HyperlinkedModelSerializer):

    modified_by = serializers.CharField(required=False)

    class Meta:
        model = Policies
        fields = ['file_name', 'policy_file', 'modified', 'modified_by']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            modified_by = request.user.employee
        else:
            raise ValidationError("No Employee given!")
        validated_data['modified_by'] = modified_by
        policy = Policies.objects.create(**validated_data)
        return policy
