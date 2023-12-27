from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from department.views import DepartmentViewSet


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename="department")

urlpatterns = [
    path('', include(router.urls)),
]
