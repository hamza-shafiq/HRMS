import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

faker = FakerFactory.create()


@register
class AssetFactory(DjangoModelFactory):
    title = factory.Sequence(lambda x: 'title{}'.format(x))
    asset_model = factory.Sequence(lambda x: 'asset_model{}'.format(x))
    asset_type = factory.Sequence(lambda x: 'asset_type{}'.format(x))
    cost = factory.Sequence(lambda x: 5000)

    class Meta:
        model = 'assets.Asset'
