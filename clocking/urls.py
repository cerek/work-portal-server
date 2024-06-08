from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from clocking.views import ClockingRecordViewSet
from clocking.views import ClockingMachineViewSet
from clocking.views import FingerRecordViewSet
from clocking.views import TimecardForEmployeeListView
from clocking.views import MyTimecardListView
from clocking.views import MyTimeCardForCalendarListView
from clocking.views import SelectBoxClockingMachineViewSet


router = DefaultRouter()
router.register(r'clockingrecord', ClockingRecordViewSet,
                basename="clocking-record")
router.register(r'clockingmachine', ClockingMachineViewSet,
                basename="clocking-machine")
router.register(r'fingerrecord', FingerRecordViewSet, basename="finger-record")

urlpatterns = [
    path('mytimecard/', MyTimecardListView.as_view(), name="my-timecard"),
    path('mytimecard-calendar/', MyTimeCardForCalendarListView.as_view(), name="my-timecard-calendar"),
    path('timecard-employee/<int:pk>/',
         TimecardForEmployeeListView.as_view(), name='timecard-employee'),
    path('selectbox/clockingmachine/',
         SelectBoxClockingMachineViewSet.as_view(), name='select-clocking-machine'),
    path('', include(router.urls)),
]
