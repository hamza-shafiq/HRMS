from django.core.exceptions import ValidationError
from rest_framework import serializers

from employees.models import Employee
from recruitments.models import Recruits, RecruitsHistory, Referrals


class RecruitsSerializer(serializers.HyperlinkedModelSerializer):
    referrers = serializers.CharField(required=False)
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = Recruits
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'phone_number', 'position', 'resume',
                  'status', 'referrers', 'full_name']

    def create(self, validated_data):
        if self.initial_data.get('referrers') is not None:
            try:
                emp = Employee.objects.filter(id=self.initial_data.get('referrers')).first()
                if emp:
                    validated_data.pop('referrers')
                    recruit = Recruits.objects.create(**validated_data)
                    Referrals.objects.create(referer=emp, recruit=recruit)
                    return recruit
                raise ValidationError('Employee with this referrer id does not exist')
            except ValidationError:
                raise ValidationError('Invalid referrer id')
        recruits = Recruits.objects.create(**validated_data)
        return recruits

    def update(self, instance, validated_data):
        referrers = Employee.objects.filter(id=validated_data.get('referrers')).first()

        if referrers:
            validated_data.pop('referrers')
            super().update(instance, validated_data)
            if len(instance.referrers.filter(recruit=instance)) == 0:
                Referrals.objects.create(recruit=instance, referer=referrers)
            else:
                instance.referrers.filter(recruit=instance).update(referer=referrers)
        if not referrers:
            super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        ret = super(RecruitsSerializer, self).to_representation(instance)
        if instance.referrers.all():
            ret['referrers'] = str(instance.referrers.all().get())
            ret['referrer_id'] = str(instance.referrers.all().get().referer_id)
        else:
            ret['referrers'] = ""
        return ret


class RecruitsHistorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = RecruitsHistory
        fields = ["id", "recruit", "process_stage", "remarks", "event_date", "conduct_by", "added_by", "added_date"]

    def to_representation(self, instance):
        ret = super(RecruitsHistorySerializer, self).to_representation(instance)
        if instance.recruit:
            ret['recruit'] = {
                'recruit_id': str(instance.recruit.id),
                'recruit_name': instance.recruit.get_full_name
            }
        if instance.added_by:
            ret['added_by'] = {
                'added_by_id': str(instance.added_by.id),
                'added_by_name': instance.added_by.get_full_name
            }
        if instance.conduct_by:
            ret['conduct_by'] = {
                'conduct_by_id': str(instance.conduct_by.id),
                'conduct_by_name': instance.conduct_by.get_full_name
            }
        return ret
