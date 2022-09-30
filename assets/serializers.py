from rest_framework import serializers
from assets.models import Asset, AssignedAsset


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    assignee = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assigned-asset-detail'
    )

    class Meta:
        model = Asset
        fields = '__all__'


class AssignedAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignedAsset
        fields = '__all__'

    def create(self, validated_data):
        return AssignedAsset.objects.create(**validated_data)