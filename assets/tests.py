from django.test import TestCase

from models import Asset


class AssetTests(TestCase):
    def test_asset_is_created_successfully(self):
        asset = Asset(
            asset_model='2018',
            asset_type='Mac',
            cost=200000
        )
        asset.save()
