from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from schedule.views import ScheduleViewSet, ScheduleForEmployeeViewSet, SchedulePlanViewSet, SchedulePlanSyncViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet, basename="schedule")
router.register(r'scheduleplan', SchedulePlanViewSet, basename="schedule-plan")
# router.register(r'schedule-employee', ScheduleForEmployeeViewSet, basename="schedule-employee")

urlpatterns = [
    path('scheduleplan/sync/<int:pk>/', SchedulePlanSyncViewSet.as_view(), name='schedule-plan-sync'),
    path('schedule-employee/<int:pk>/',
         ScheduleForEmployeeViewSet.as_view(), name='schedule-employee'),
    path('', include(router.urls)),
]
