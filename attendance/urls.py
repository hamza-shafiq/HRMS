from django.urls import path

from attendance.views import AttendanceViewSet, LeavesViewSet

attendance_list = AttendanceViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
attendance_detail = AttendanceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
leaves_list = LeavesViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
leaves_detail = LeavesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
mark_attendance = AttendanceViewSet.as_view({
    'post': 'mark_attendance'
})

urlpatterns = [
    path('attendance/', attendance_list, name="attendance-list"),
    path('attendance/<str:pk>/', attendance_detail, name='attendance-detail'),
    path('leaves/', leaves_list, name="leaves-list"),
    path('leaves/<str:pk>/', leaves_detail, name='leaves-detail'),
    path('mark-attendance/', mark_attendance, name='mark-attendance')
]
