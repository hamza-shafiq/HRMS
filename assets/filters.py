import django_filters
from django_filters import filters

from assets.models import Asset


class AssetFilter(django_filters.FilterSet):
    status = filters.CharFilter(
        method='filter_asset_status',
    )

    class Meta:
        model = Asset
        fields = ['status']

    def filter_asset_status(self, queryset, name, value):
        return queryset.filter(status=value)
