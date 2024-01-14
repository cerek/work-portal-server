from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from permission.views import PermissionViewSet, PermissionEmployeeRetrieveView, PermissionEmployeeUpdateView, PermissionDepartmentRetrieveView, PermissionDepartmentUpdateView

router = DefaultRouter()
router.register(r'permission', PermissionViewSet, basename="permission")

urlpatterns = [
    path("permission/employee/<int:pk>/", PermissionEmployeeRetrieveView.as_view(), name="permission-employee-detail"),
    path("permission-update/employee/<int:pk>/", PermissionEmployeeUpdateView.as_view(), name="permission-employee-update"),
    path("permission/department/<int:pk>/", PermissionDepartmentRetrieveView.as_view(), name="permission-department-detail"),
    path("permission-update/department/<int:pk>/", PermissionDepartmentUpdateView.as_view(), name="permission-department-update"),
    path('', include(router.urls)),
]
