from rest_framework import serializers
from systemlogs.models import Systemlogs


class SystemlogsSerializer(serializers.ModelSerializer):
    systemlog_operator_hm = serializers.SerializerMethodField()
    systemlog_operator_dept_hm = serializers.SerializerMethodField()
    systemlog_request_method_hm = serializers.SerializerMethodField()

    class Meta:
        model = Systemlogs
        fields = '__all__'

    def get_systemlog_operator_hm(self, obj):
        return obj.systemlog_operator.employee.username

    def get_systemlog_operator_dept_hm(self, obj):
        return obj.systemlog_operator.employee_department.department.name

    def get_systemlog_request_method_hm(self, obj):
        return obj.get_systemlog_request_method_display()
