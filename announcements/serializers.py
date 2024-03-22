from django.core.exceptions import ValidationError
from rest_framework import serializers

from announcements.models import Announcements


class AnnouncementsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Announcements
        fields = ['id', 'title', 'detail', 'added_date', 'added_by', 'date_from', 'date_to']

    def to_representation(self, instance):
        ret = super(AnnouncementsSerializer, self).to_representation(instance)
        if instance.added_by:
            ret['added_by'] = {
                'added_by_id': str(instance.added_by.id),
                'added_by_name': instance.added_by.get_full_name
            }

        return ret
