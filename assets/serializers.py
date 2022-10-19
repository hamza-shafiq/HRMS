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
        fields = ["url", "assignee", "id", "title", "description", "asset_model", "asset_type", "cost"]


class AssignedAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignedAsset
        fields = ["id", "asset", "employee"]

    def create(self, validated_data):
        return AssignedAsset.objects.create(**validated_data)
