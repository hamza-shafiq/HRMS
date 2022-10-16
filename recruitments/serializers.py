from rest_framework import serializers
from employees.models import Employee
from recruitments.models import Recruits, Referrals


class RecruitsSerializer(serializers.HyperlinkedModelSerializer):
    referrers = serializers.CharField(required=False)

    class Meta:
        model = Recruits
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'phone_number', 'position', 'resume', 'status', 'referrers']

    def create(self, validated_data):
        if self.initial_data.get('referrers') is not None:
            try:
                emp = Employee.objects.filter(id=self.initial_data.get('referrers')).first()
                if emp:
                    validated_data.pop('referrers')
                    recruit = Recruits.objects.create(**validated_data)
                    Referrals.objects.create(referer=emp, recruit=recruit)
                    return recruit
                raise serializers.ValidationError(
                    self.default_error_messages['Employee with this referrer id does not exist'])
            except Exception as e:
                raise serializers.ValidationError(
                    self.default_error_messages['Invalid referrer id'])
        recruits = Recruits.objects.create(**validated_data)
        return recruits
