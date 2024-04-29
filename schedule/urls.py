from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from schedule.views import ScheduleViewSet, ScheduleForEmployeeViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet, basename="schedule")
# router.register(r'schedule-employee', ScheduleForEmployeeViewSet, basename="schedule-employee")

urlpatterns = [
    path('schedule-employee/<int:pk>/',
         ScheduleForEmployeeViewSet.as_view(), name='schedule-employee'),
    path('', include(router.urls)),
]
