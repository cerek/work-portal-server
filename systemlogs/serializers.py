from rest_framework import serializers
from systemlogs.models import Systemlogs


class SystemlogsSerializer(serializers.ModelSerializer):
    systemlog_request_method_hm = serializers.SerializerMethodField()

    class Meta:
        model = Systemlogs
        fields = '__all__'

    def get_systemlog_request_method_hm(self, obj):
        return obj.get_systemlog_request_method_display()
