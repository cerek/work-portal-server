from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from location.views import LocationViewSet
from location.views import SelectBoxLocationViewSet


router = DefaultRouter()
router.register(r'location', LocationViewSet, basename="location")

urlpatterns = [
    path('selectbox/location/', SelectBoxLocationViewSet.as_view(), name='select-location'),
    path('', include(router.urls)),
]
