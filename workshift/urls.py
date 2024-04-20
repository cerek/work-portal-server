from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from workshift.views import WorkShiftViewSet, SelectBoxWorkShiftViewSet

router = DefaultRouter()
router.register(r'workshift', WorkShiftViewSet, basename="work-shift")

urlpatterns = [
    path('selectbox/workshift/', SelectBoxWorkShiftViewSet.as_view(), name='select-work-shift'),
    path('', include(router.urls)),
]
