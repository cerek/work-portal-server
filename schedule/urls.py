from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from schedule.views import ScheduleViewSet, MyScheduleViewSet, ScheduleForEmployeeViewSet, SchedulePlanViewSet, MyScheduleChangeViewSet, SchedulePlanSyncViewSet, ScheduleChangeViewSet, ScheduleChangeDecideViewSet


router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet, basename="schedule")
router.register(r'scheduleplan', SchedulePlanViewSet, basename="schedule-plan")
router.register(r'schedulechange', ScheduleChangeViewSet, basename="schedule-change")
router.register(r'myschedulechange', MyScheduleChangeViewSet, basename="myschedule-change")


urlpatterns = [
    path('myschedule/', MyScheduleViewSet.as_view(), name="myschedule"),
    path('schedulechange/decide/<int:pk>/', ScheduleChangeDecideViewSet.as_view(), name='schedule-change-decide'),
    path('scheduleplan/sync/<int:pk>/', SchedulePlanSyncViewSet.as_view(), name='schedule-plan-sync'),
    path('schedule-employee/<int:pk>/',
         ScheduleForEmployeeViewSet.as_view(), name='schedule-employee'),
    path('', include(router.urls)),
]
