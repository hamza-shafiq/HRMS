from django.urls import include, path
from rest_framework.routers import DefaultRouter
from finance.views import PayRollViewSet


router = DefaultRouter()
router.register(r'payroll', PayRollViewSet, basename="payroll")

urlpatterns = [
    path('', include(router.urls)),
]
