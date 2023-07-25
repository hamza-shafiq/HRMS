from django.core.exceptions import ValidationError
from rest_framework import serializers
from policies.models import Policies


class PolicySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Policies
        fields = ['file_name', 'policy_file']
