from django.contrib.auth.models import User
from rest_framework import serializers
from employee.models import Employee
from department.models import Department
from department.serializers import DepartmentSerializer
from location.models import Location
from location.serializers import LocationSerializer


class UserSerializer(serializers.ModelSerializer):
    is_active_hm = serializers.SerializerMethodField()
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_is_active_hm(self, obj):
        if obj.is_active:
            return "Active"
        else:
            return "Suspend"

    def create(self, validated_data):
        password = validated_data.pop('password')
        new_user = User.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user

class EmployeeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    employee_department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    employee_work_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    employee_onboard_days = serializers.SerializerMethodField()
    employee_gender_hm = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
        depth = 2

    def get_employee_onboard_days(self, obj):
        return obj.calculate_day_onboard()

    def get_employee_gender_hm(self, obj):
        return obj.get_employee_gender_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Serialzier the department information from PrimaryKeyRelatedField
        if ret['employee_department'] is not None:
            dept_serializer = DepartmentSerializer(Department.objects.get(pk=ret['employee_department']))
            ret['employee_department'] = dept_serializer.data

        # Serialzier the location information from PrimaryKeyRelatedField
        if ret['employee_work_location'] is not None:
            location_serializer = LocationSerializer(Location.objects.get(pk=ret['employee_work_location']))
            ret['employee_work_location'] = location_serializer.data

        return ret

    def create(self, validated_data):
        user_data = validated_data.pop('employee', {})
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                new_user = user_serializer.save()
                if 'employee_department' in validated_data:
                    new_user.groups.add(
                        validated_data['employee_department'].department)
            except Exception as e:
                raise serializers.ValidationError({"error": e.args})
        new_employee = Employee.objects.create(
            employee=new_user, **validated_data)
        return new_employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop('employee', {})
        user_instance = instance.employee
        # Prevent to modify the user password
        if 'password' in user_data:
            user_data.pop('password')
        # Update the user instance
        if user_data:
            for k,v in user_data.items():
                setattr(user_instance, k, v)
        user_instance.save()
        # Update the user-group relation
        if 'employee_department' in validated_data:
            user_instance.groups.clear()
            user_instance.groups.add(validated_data['employee_department'].department)

        return super().update(instance, validated_data)



class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class EmployeeContactSerializer(serializers.ModelSerializer):
    employee = UserContactSerializer()
    employee_department = serializers.StringRelatedField()
    employee_work_location = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['employee', 'employee_job_title', 'employee_num', 'employee_phone',
                  'employee_extension', 'employee_department', 'employee_work_location']


class EmployeeChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = ['password', 'password2', 'old_password']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        employee_user = instance.employee
        if user != employee_user:
            raise serializers.ValidationError(
                {"error": "You only can change own password!"})
        employee_user.set_password(validated_data['password'])
        employee_user.save()
        return instance


class EmployeeChangePasswordAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = ['password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data

    def update(self, instance, validated_data):
        employee_user = instance.employee
        employee_user.set_password(validated_data['password'])
        employee_user.save()
        return instance


class UserSelectBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class EmployeeSelectBoxSerializer(serializers.ModelSerializer):
    employee = UserSelectBoxSerializer(required=False)

    class Meta:
        model = Employee
        fields = ['id', 'employee']
