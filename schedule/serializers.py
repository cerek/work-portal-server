from rest_framework import serializers
from schedule.models import Schedule, SchedulePlan


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_employee_name_hm = serializers.SerializerMethodField()
    schedule_work_shift_hm = serializers.SerializerMethodField()
    schedule_work_start_datetime_hm = serializers.SerializerMethodField()
    schedule_work_end_datetime_hm = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = '__all__'

    def get_schedule_employee_name_hm(self, obj):
        res_name = f"{obj.schedule_employee.employee.first_name.capitalize()} {obj.schedule_employee.employee.last_name.capitalize()}"
        return res_name

    def get_schedule_work_shift_hm(self, obj):
        res_shift = f"{obj.schedule_work_shift.shift_start_time} - {obj.schedule_work_shift.shift_end_time}"
        return res_shift

    def get_schedule_work_start_datetime_hm(self, obj):
        return f"{obj.schedule_date} {obj.schedule_work_shift.shift_start_time}"

    def get_schedule_work_end_datetime_hm(self, obj):
        return f"{obj.schedule_date} {obj.schedule_work_shift.shift_end_time}"

    def create(self, validated_data):
        print(validated_data)
        try:
            new_schedule, _ = Schedule.objects.get_or_create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": e.args})
        return new_schedule


class SchedulePlanSerializer(serializers.ModelSerializer):
    schedule_plan_employee_hm = serializers.SerializerMethodField()
    schedule_plan_work_shift_hm = serializers.SerializerMethodField()
    schedule_plan_status_hm = serializers.SerializerMethodField()

    class Meta:
        model = SchedulePlan
        fields = '__all__'

    def get_schedule_plan_employee_hm(self, obj):
        res_employee_name_list = []
        plan_employee_list = obj.schedule_plan_employee.all()
        if plan_employee_list.count() != 0:
            res_employee_name_list = [x['employee__username'] for x in plan_employee_list.values('employee__username')]
        return res_employee_name_list

    def get_schedule_plan_status_hm(self, obj):
        return obj.get_schedule_plan_status_display()

    def get_schedule_plan_work_shift_hm(self, obj):
        res_shift = f"{obj.schedule_plan_work_shift.shift_start_time} - {obj.schedule_plan_work_shift.shift_end_time}"
        return res_shift
