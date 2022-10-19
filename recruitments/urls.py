from django.urls import path
from recruitments.views import RecruitsViewSet

recruits_list = RecruitsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
recruits_detail = RecruitsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('recruits/', recruits_list, name="recruits-list"),
    path('recruits/<str:pk>/', recruits_detail, name='recruits-detail'),
]
