from rest_framework import serializers

from employees.models import Employee
from recruitments.models import Recruits, Referrals


class RecruitsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recruits
        fields = '__all__'

    def create(self, validated_data):
        recruits = Recruits.objects.create(**validated_data)
        if self.initial_data.get('referrers'):
            emp = Employee.objects.get(id=self.initial_data.get('referrers'))
            if emp:
                Referrals.objects.create(referer=emp, recruit=recruits)
        return recruits

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        referrers = instance.referrers.all()
        if referrers.exists():
            ret["referrer"] = referrers.first().id
        return ret