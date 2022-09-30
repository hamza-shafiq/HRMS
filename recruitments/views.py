from .serializers import RecruitsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from recruitments.models import Recruits, Referrals
# Create your views here.


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Recruits.objects.all()
    serializer_class = RecruitsSerializer
