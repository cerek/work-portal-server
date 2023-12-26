from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from location.views import LocationViewSet


router = DefaultRouter()
router.register(r'location', LocationViewSet, basename="location")

urlpatterns = [
    path('', include(router.urls)),
]
