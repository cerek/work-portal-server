from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from timeoff.views import TimeoffViewSet, TimeoffApplicationViewSet, MyTimeoffApplicationViewSet, MyTimeoffViewSet, TimeoffTypeViewSet, TimeoffApplicationDecideViewSet, TimeoffForEmployeeViewSet, SelectBoxTimeoffTypeViewSet

router = DefaultRouter()
router.register(r'timeoffapplication', TimeoffApplicationViewSet, basename="timeoffapplication")
router.register(r'mytimeoffapplication', MyTimeoffApplicationViewSet, basename="mytimeoffapplication")
router.register(r'timeoff', TimeoffViewSet, basename="timeoff")
router.register(r'timeofftype', TimeoffTypeViewSet, basename="timeoff-type")

urlpatterns = [
    path('mytimeoff/', MyTimeoffViewSet.as_view(), name='mytimeoff'),
    path('timeoffapplication/decide/<int:pk>/', TimeoffApplicationDecideViewSet.as_view(), name='timeoff-application-decide'),
    path('timeoff-employee/<int:pk>/',
         TimeoffForEmployeeViewSet.as_view(), name='timeoff-employee'),
    path('selectbox/timeofftype/', SelectBoxTimeoffTypeViewSet.as_view(), name='select-timeoff-type'),
    path('', include(router.urls)),
]
