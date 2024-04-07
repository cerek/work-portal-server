from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from task.views import WorkPeriodicTaskViewSet, ClockedScheduleViewSet, IntervalScheduleViewSet, CrontabScheduleViewSet
from task.views import SelectBoxClockedViewSet, SelectBoxCrontabViewSet, SelectBoxIntervalViewSet


router = DefaultRouter()
router.register(r'task', WorkPeriodicTaskViewSet, basename="task")
router.register(r'clocked-schedule', ClockedScheduleViewSet, basename="clocked-schedule")
router.register(r'interval-schedule', IntervalScheduleViewSet, basename="interval-schedule")
router.register(r'crontab-schedule', CrontabScheduleViewSet, basename="crontab-schedule")

urlpatterns = [
    path('selectbox/clocked/', SelectBoxClockedViewSet.as_view(), name='select-clocked'),
    path('selectbox/crontab/', SelectBoxCrontabViewSet.as_view(), name='select-crontab'),
    path('selectbox/interval/', SelectBoxIntervalViewSet.as_view(), name='select-interval'),
    path('', include(router.urls)),
]
