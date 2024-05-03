from rest_framework import serializers
from workshift.models import WorkShift


class WorkShiftSerializer(serializers.ModelSerializer):
    shift_status_hm = serializers.SerializerMethodField()

    class Meta:
        model = WorkShift
        fields = '__all__'

    def get_shift_status_hm(self, obj):
        return obj.get_shift_status_display()


class SelectBoxWorkShiftSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = WorkShift
        fields = ['id', 'value']

    def get_value(self, obj):
        res_work_shift = f'{obj.shift_name}({obj.shift_start_time} - {obj.shift_end_time})'
        return res_work_shift