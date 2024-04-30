from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hrms.pagination import CustomPageNumberPagination
from announcements.models import Announcements
from rest_framework.decorators import action

from .permissions import AnnouncementsPermission
from announcements.serializers import AnnouncementsSerializer


class AnnouncementsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AnnouncementsPermission]
    queryset = Announcements.objects.filter(is_deleted=False)
    serializer_class = AnnouncementsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPageNumberPagination

    @action(detail=False, url_path="latest", methods=['get'])
    def latest(self, request):
        try:
            latest_announcement = Announcements.objects.latest('added_date')
            title = latest_announcement.title
            latest_detail = latest_announcement.detail
            data = [{'title': title, 'latest_detail': latest_detail}]
            return JsonResponse(data=data, safe=False)
        except Announcements.DoesNotExist:
            return JsonResponse({'error': 'No announcements found'}, status=404)
