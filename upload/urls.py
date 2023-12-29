from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from upload.views import UploadViewSet


router = DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")

urlpatterns = [
    path('', include(router.urls)),
]
