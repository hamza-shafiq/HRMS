from django.urls import include, path
from rest_framework.routers import DefaultRouter

from policies.views import PoliciesViewSet

router = DefaultRouter()
router.register(r'policies', PoliciesViewSet, basename="policies")

urlpatterns = [
    path('', include(router.urls)),
]
