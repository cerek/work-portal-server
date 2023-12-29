from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from employee.views import EmployeeViewSet
from employee.views import EmployeeProfileViewSet
from employee.views import EmployeeContactListView
from employee.views import EmployeeChangePasswordView
from employee.views import EmployeeChangePasswordAdminView
from employee.views import EmployeeSelectBoxListView


router = DefaultRouter()
router.register(r'employee', EmployeeViewSet, basename="employee")

urlpatterns = [
    path('employee/admin-change-password/<int:pk>/',
         EmployeeChangePasswordAdminView.as_view(), name='employee-admin-change-password'),
    path('employee/change-password/<int:pk>/',
         EmployeeChangePasswordView.as_view(), name='employee-change-password'),
    path('employee/profile/<int:pk>/',
         EmployeeProfileViewSet.as_view(), name='employee-profile'),
    path('employee/contact/', EmployeeContactListView.as_view(),
         name='employee-contact'),
    path('employee/selectbox/', EmployeeSelectBoxListView.as_view(),
         name='employee-selectbox'),
    path('', include(router.urls)),
]
