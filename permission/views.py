from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from permission.serializers import PermissionSerializer, PermissionEmployeeSerializer, PermissionDepartmentSerializer
from permission.permissions import ViewEmployeePermission, ViewDepartmentPermission
from employee.models import Employee
from department.models import Department
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ['name', 'codename', ]
    search_fields = ['name', 'codename', ]
    pagination_class = StandardResultsSetPagination


class PermissionEmployeeRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & ViewEmployeePermission]
    queryset = Employee.objects.all()
    serializer_class = PermissionEmployeeSerializer


class PermissionEmployeeUpdateView(UpdateAPIView):
    permission_class = [IsAuthenticated & ExtendViewPermission]
    queryset = Employee.objects.all()
    serializer_class = PermissionEmployeeSerializer

    def update(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=kwargs.get('pk'))
        update_permission_list = request.data.get('permissions', None)
        if update_permission_list is None:
            raise serializers.ValidationError({"permission": ["The field is required."]})
        new_permission = Permission.objects.filter(id__in=update_permission_list)

        try:
            # Clear all the employee permission
            employee.employee.user_permissions.clear()
            # Update the permission for employee
            employee.employee.user_permissions.add(*new_permission)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        ret_serializer = PermissionEmployeeSerializer(employee)
        return Response(ret_serializer.data)


class PermissionDepartmentRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & ViewDepartmentPermission]
    queryset = Department.objects.all()
    serializer_class = PermissionDepartmentSerializer


class PermissionDepartmentUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated & ExtendViewPermission]
    queryset = Department.objects.all()

    def update(self, request, *args, **kwargs):
        department = Department.objects.get(pk=kwargs.get('pk'))
        update_permission_list = request.data.get('permissions', None)
        if update_permission_list is None:
            raise serializers.ValidationError({"permission": ["The field is required."]})
        new_permission = Permission.objects.filter(id__in=update_permission_list)

        try:
            # Clear all the department permission
            department.department.permissions.clear()
            # Update the permission for department
            department.department.permissions.add(*new_permission)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        ret_serializer = PermissionDepartmentSerializer(department)
        return Response(ret_serializer.data)