from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from employee.models import Employee
from department.models import Department


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        depth = 2

class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'user_permissions']

class PermissionEmployeeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    class Meta:
        model = Employee
        fields = ['employee']
        depth = 2


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def get_permissions(self, obj):
        group_permission = obj.permissions.all()
        return [x.codename for x in group_permission]


class PermissionDepartmentSerializer(serializers.ModelSerializer):
    department = GroupSerializer()
    class Meta:
        model = Department
        fields = ['id', 'department']