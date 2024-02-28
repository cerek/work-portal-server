from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from timeoff.views import TimeoffViewSet, MyTimeoffViewSet, TimeoffTypeViewSet, SelectBoxTimeoffTypeViewSet

router = DefaultRouter()
router.register(r'timeoff', TimeoffViewSet, basename="timeoff")
router.register(r'mytimeoff', MyTimeoffViewSet, basename="mytimeoff")
router.register(r'timeofftype', TimeoffTypeViewSet, basename="timeoff-type")

urlpatterns = [
    path('selectbox/timeofftype/', SelectBoxTimeoffTypeViewSet.as_view(), name='select-ticket-type'),
    path('', include(router.urls)),
]
