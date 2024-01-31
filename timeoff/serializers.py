from rest_framework import serializers
from timeoff.models import Timeoff, TimeoffType
from employee.models import Employee
from datetime import datetime, timedelta, timezone


class TimeoffSerializer(serializers.ModelSerializer):
    timeoff_apply_employee_hm = serializers.SerializerMethodField()
    timeoff_apply_employee_department_hm = serializers.SerializerMethodField()
    timeoff_approval_employee_hm = serializers.SerializerMethodField()
    timeoff_status_hm = serializers.SerializerMethodField()
    timeoff_type_hm = serializers.SerializerMethodField()
    timeoff_hours = serializers.SerializerMethodField()
    class Meta:
        model = Timeoff
        fields = '__all__'

    def get_timeoff_apply_employee_hm(self, obj):
        apply_employee = Employee.objects.get(pk=obj.timeoff_apply_employee.id)
        return apply_employee.employee.username

    def get_timeoff_apply_employee_department_hm(self, obj):
        apply_employee_department = Employee.objects.get(pk=obj.timeoff_apply_employee.id)
        return apply_employee_department.employee_department.department.name

    def get_timeoff_approval_employee_hm(self, obj):
        res_approval_name = ""
        if obj.timeoff_approval_employee:
            approval_employee = Employee.objects.get(pk=obj.timeoff_approval_employee.id)
            res_approval_name = approval_employee.employee.username
        return res_approval_name

    def get_timeoff_type_hm(self, obj):
        timeoff_type = TimeoffType.objects.get(pk=obj.timeoff_type.id)
        return timeoff_type.timeoff_type_name

    def get_timeoff_status_hm(self, obj):
        return obj.get_timeoff_status_display()

    def get_timeoff_hours(self, obj):
        return obj.gain_timeoff_hours()


class MyTimeoffSerializer(serializers.ModelSerializer):
    timeoff_apply_employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    timeoff_apply_employee_hm = serializers.SerializerMethodField()
    timeoff_approval_employee_hm = serializers.SerializerMethodField()
    timeoff_status_hm = serializers.SerializerMethodField()
    timeoff_type_hm = serializers.SerializerMethodField()
    timeoff_hours = serializers.SerializerMethodField()
    class Meta:
        model = Timeoff
        fields = '__all__'

    def get_timeoff_apply_employee_hm(self, obj):
        apply_employee = Employee.objects.get(pk=obj.timeoff_apply_employee.id)
        return apply_employee.employee.username

    def get_timeoff_approval_employee_hm(self, obj):
        res_approval_name = ""
        if obj.timeoff_approval_employee:
            approval_employee = Employee.objects.get(pk=obj.timeoff_approval_employee.id)
            res_approval_name = approval_employee.employee.username
        return res_approval_name

    def get_timeoff_type_hm(self, obj):
        timeoff_type = TimeoffType.objects.get(pk=obj.timeoff_type.id)
        return timeoff_type.timeoff_type_name

    def get_timeoff_status_hm(self, obj):
        return obj.get_timeoff_status_display()

    def get_timeoff_hours(self, obj):
        return obj.gain_timeoff_hours()

    def create(self, validated_data):
        user = self.context['request'].user
        for deny_field in ['timeoff_approval_employee', 'timeoff_status']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't submit with {deny_field}"})
        new_timeoff = Timeoff.objects.create(timeoff_apply_employee=user.employee, **validated_data)
        return new_timeoff

    def update(self, instance, validated_data):
        for deny_field in ['timeoff_approval_employee', 'timeoff_apply_employee']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't submit with {deny_field}"})
        if 'timeoff_status' in validated_data.keys():
            if validated_data['timeoff_status'] not in [4]:
                raise serializers.ValidationError({'timeoff_status': 'Regular Employee only can "Cancel" the timeoff !!!'})
        if 'timeoff_end_datetime' in validated_data.keys():
            # Need to enhance the timezone
            now_time = datetime.now(timezone(timedelta(hours=-8)))
            days_diff = (instance.timeoff_end_datetime - now_time).days
            if days_diff < 1:
                raise serializers.ValidationError({'timeoff_end_datetime': 'You can modify the timeoff less one day!!!'})
            return super().update(instance, validated_data)


class TimeoffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeoffType
        fields = '__all__'