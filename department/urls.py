from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from department.views import DepartmentViewSet
from department.views import SelectBoxDepartmentViewSet


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename="department")

urlpatterns = [
    path('selectbox/department/', SelectBoxDepartmentViewSet.as_view(), name='select-department'),
    path('', include(router.urls)),
]
