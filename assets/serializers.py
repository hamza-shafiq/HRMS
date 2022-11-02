from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from assets.models import Asset, AssignedAsset


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    assignee = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assigned-asset-detail'
    )

    class Meta:
        model = Asset
        fields = ["url", "assignee", "id", "title", "description", "asset_model", "asset_type", "cost"]


class AssignedAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignedAsset
        fields = ["id", "asset", "employee"]

    def create(self, validated_data):
        record = AssignedAsset.objects.filter(asset=validated_data['asset'])
        if record:
            raise ValidationError('This asset is already assigned to someone')
        return super().create(validated_data)
