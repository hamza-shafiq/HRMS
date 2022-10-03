from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.response import Response

from employees.models import Employee
from recruitments.models import Recruits, Referrals


class RecruitsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recruits
        fields = '__all__'

    def create(self, validated_data):
        if self.initial_data.get('referrers'):
            try:
                emp = Employee.objects.filter(id=self.initial_data.get('referrers'))
                if emp.first():
                    recruits = Recruits.objects.create(**validated_data)
                    Referrals.objects.create(referer=emp.first(), recruit=recruits)
                    return recruits
                raise serializers.ValidationError(
                    self.default_error_messages['Employee with this referrer id does not exist'])
            except Exception as e:
                raise serializers.ValidationError(
                    self.default_error_messages['Invalid Referrer id'])
        raise serializers.ValidationError(
                    self.default_error_messages['Referrer id is not provided'])