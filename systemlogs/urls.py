from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from systemlogs.views import SystemlogsViewSet


router = DefaultRouter()
router.register(r'systemlogs', SystemlogsViewSet, basename="systemlogs")

urlpatterns = [
    path('', include(router.urls)),
]
