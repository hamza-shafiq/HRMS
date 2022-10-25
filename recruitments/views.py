from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import RecruitsSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import RecruitsPermission
from rest_framework import viewsets, status
from recruitments.models import Recruits


class RecruitsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RecruitsPermission]
    queryset = Recruits.objects.filter(is_deleted=False)
    serializer_class = RecruitsSerializer

    def destroy(self, request, *args, **kwargs):
        recruit = self.get_object()
        recruit.is_deleted = True
        recruit.save()
        return Response(data=f'Recruit {recruit.first_name} {recruit.last_name} deleted successfully')

    def list(self, request, *args, **kwargs):
        recruit_id = self.request.query_params.get('id')
        serializer_context = {
            'request': request,
        }
        if recruit_id:
            try:
                record = Recruits.objects.filter(id=recruit_id, is_deleted=False)
            except:
                return JsonResponse({'error': 'Invalid Recruit id'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer = RecruitsSerializer(record, many=True, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Recruits.objects.all()
        serializer = RecruitsSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
