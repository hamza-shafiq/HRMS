from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from assets.models import Asset, AssetStatus, AssignedAsset
from employees.models import Employee


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    assignee = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Asset
        fields = ["url", "id", "title", "description", "asset_model", "asset_type", "cost", "asset_image",
                  "status", "assignee"]

    def create(self, validated_data):
        assignee = validated_data.pop('assignee')
        if assignee:
            assignee = Employee.objects.get(id=assignee)
            validated_data['status'] = AssetStatus.ASSIGNED
        asset = Asset.objects.create(**validated_data)
        if assignee:
            AssignedAsset.objects.create(asset=asset, employee=assignee)
        return asset

    def update(self, instance, validated_data):
        if 'assignee' in validated_data:
            assignee = validated_data.pop('assignee')
            if assignee:
                validated_data['status'] = AssetStatus.ASSIGNED
                assignee = Employee.objects.get(id=assignee)
                AssignedAsset.objects.create(asset=instance, employee=assignee)
            else:
                validated_data['status'] = AssetStatus.UNASSIGNED
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        ret = super(AssetSerializer, self).to_representation(instance)
        ret['assignee'] = None
        if instance.status == AssetStatus.ASSIGNED and instance.assignee.all():
            ret['assignee'] = {
                "assignee_name": str(instance.assignee.all().last().employee.get_full_name),
                "assignee_id": str(instance.assignee.all().last().employee_id)
            }
            ret["assign_asset_id"] = str(instance.assignee.all().last().id)
        return ret


class AssignedAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignedAsset
        fields = ["id", "asset", "employee"]

    def create(self, validated_data):
        record = AssignedAsset.objects.filter(asset=validated_data['asset'])
        if record:
            raise ValidationError('This asset is already assigned to someone')
        return super().create(validated_data)
