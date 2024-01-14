from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.serializers import EmployeeContactSerializer
from employee.serializers import EmployeeChangePasswordSerializer
from employee.serializers import EmployeeChangePasswordAdminSerializer
from employee.serializers import EmployeeSelectBoxSerializer
from rest_framework.permissions import IsAuthenticated
from employee.permissions import ViewProfile, IsOwner, ViewContactPermission, ChangePasswordAdminPermission
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['employee__username', 'employee__first_name',
                        'employee__last_name', 'employee_job_title', 'employee_department__department__name']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name',
                     'employee_job_title', 'employee_department__department__name']
    pagination_class = StandardResultsSetPagination

    def destroy(self, request, *args, **kwargs):
        delete_obj = self.get_object()
        obj_serializer = self.get_serializer(self.get_object()).data

        # Using the delete() with User object, the related Employee object will be deleted
        # oppositely, User object will not be deleted by invoke the Employee.delete()
        # That's why annotate the super().destroy() function below.
        if delete_obj.employee:
            try:
                delete_obj.employee.delete()
            except Exception as e:
                return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        # Return the deleted object to client.
        return Response(obj_serializer, status=status.HTTP_200_OK)


class EmployeeProfileViewSet(RetrieveAPIView):
    permission_classes = [IsAuthenticated & ViewProfile]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeContactListView(ListAPIView):
    permission_classes = [IsAuthenticated & ViewContactPermission]
    serializer_class = EmployeeContactSerializer

    # Overwirte the get_queryset to filter the contact of employee's own department
    def get_queryset(self):
        ALL_CONTACT = self.request.query_params.get('all', 0)
        # if employee has view_employee_all_contact permission, he/she can retrieve all the contact
        # if not, only his/her department contact will be reture
        if int(ALL_CONTACT) == 1 and self.request.user.has_perm('employee.view_employee_all_contact'):
            queryset = Employee.objects.all()
            return queryset
        employee_dept = self.request.user.employee.employee_department
        queryset = Employee.objects.filter(employee_department=employee_dept)
        return queryset


class EmployeeChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsOwner]
    queryset = Employee.objects.all()
    serializer_class = EmployeeChangePasswordSerializer


class EmployeeChangePasswordAdminView(UpdateAPIView):
    permission_classes = [IsAuthenticated & ChangePasswordAdminPermission]
    queryset = Employee.objects.all()
    serializer_class = EmployeeChangePasswordAdminSerializer


class EmployeeSelectBoxListView(ListAPIView):
    permission_classes = [ExtendViewPermission]
    serializer_class = EmployeeSelectBoxSerializer
    queryset = Employee.objects.all()
    pagination_class = StandardResultsSetPagination
