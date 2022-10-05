from rest_framework.response import Response
from .serializers import RecruitsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from recruitments.models import Recruits


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Recruits.objects.filter(is_deleted=False)
    serializer_class = RecruitsSerializer

    def destroy(self, request, *args, **kwargs):
        recruit = self.get_object()
        recruit.is_deleted = True
        recruit.save()
        return Response(data=f'Recruit {recruit.first_name} {recruit.last_name} deleted successfully')
