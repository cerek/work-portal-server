from django.utils import timezone
from rest_framework import serializers
from timeoff.models import TimeoffApplication, Timeoff, TimeoffType
from employee.models import Employee
from schedule.models import Schedule
from datetime import timedelta


class TimeoffApplicationSerializer(serializers.ModelSerializer):
    timeoff_application_applicant_hm = serializers.SerializerMethodField()
    timeoff_application_applicant_dept_hm = serializers.SerializerMethodField()
    timeoff_application_approver_hm = serializers.SerializerMethodField()
    timeoff_application_status_hm = serializers.SerializerMethodField()
    timeoff_application_type_hm = serializers.SerializerMethodField()
    timeoff_application_total_hours = serializers.SerializerMethodField()

    class Meta:
        model = TimeoffApplication
        fields = '__all__'

    def get_timeoff_application_applicant_hm(self, obj):
        res_name = f"{obj.timeoff_application_applicant.employee.first_name.capitalize()} {obj.timeoff_application_applicant.employee.last_name.capitalize()}"
        return res_name

    def get_timeoff_application_applicant_dept_hm(self, obj):
        res_dept = obj.timeoff_application_applicant.employee_department.department.name
        return res_dept

    def get_timeoff_application_approver_hm(self, obj):
        res_name = '-'
        if obj.timeoff_application_approver:
            res_name = f"{obj.timeoff_application_approver.employee.first_name.capitalize()} {obj.timeoff_application_approver.employee.last_name.capitalize()}"
        return res_name

    def get_timeoff_application_status_hm(self, obj):
        return obj.get_timeoff_application_status_display()
    
    def get_timeoff_application_type_hm(self, obj):
        res = obj.timeoff_application_type.timeoff_type_name
        return res

    def get_timeoff_application_total_hours(self, obj):
        return 0


class MyTimeoffApplicationSerializer(TimeoffApplicationSerializer):
    timeoff_application_applicant = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta:
        model = TimeoffApplication
        fields = '__all__'

    def create(self, validated_data):
        deny_field_list = ['timeoff_application_applicant', 'timeoff_application_approver', 'timeoff_application_status', 'timeoff_application_reject_reason']
        user = self.context['request'].user
        for deny_field in deny_field_list:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't submit with {deny_field}"})
        new_timeoffapplication = TimeoffApplication.objects.create(timeoff_application_applicant=user.employee, **validated_data)
        return new_timeoffapplication

    def update(self, instance, validated_data):
        deny_field_list = ['timeoff_application_applicant', 'timeoff_application_approver', 'timeoff_application_reject_reason']
        for deny_field in deny_field_list:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't submit with {deny_field}"})
        if 'timeoff_application_status' in validated_data.keys():
            if validated_data['timeoff_application_status'] not in [4]:
                raise serializers.ValidationError({'timeoff_application_status': 'Regular Employee only can "Cancel" the timeoff application request !!!'})
        return super().update(instance, validated_data)


class TimeoffApplicationDecideSerializer(TimeoffApplicationSerializer):
    class Meta:
        model = TimeoffApplication
        fields = '__all__'

    def update(self, instance, validated_data):
        new_validated_data = {}
        new_validated_data['timeoff_application_status'] = validated_data.get('timeoff_application_status')
        user = self.context['request'].user
        new_validated_data['timeoff_application_approver'] = user.employee
        new_instance = super().update(instance, new_validated_data)
        if new_instance.timeoff_application_status == 5:
            return new_instance
        if new_instance.timeoff_application_status in [2, 3]:
            start_date = timezone.localdate(new_instance.timeoff_application_start_datetime)
            start_time = timezone.localtime(new_instance.timeoff_application_start_datetime).time()
            end_date = timezone.localdate(new_instance.timeoff_application_end_datetime)
            end_time = timezone.localtime(new_instance.timeoff_application_end_datetime).time()
            timeoff_days = (end_date - start_date).days
            if start_date == end_date:
                check_schedule_qs = Schedule.objects.filter(schedule_employee=new_instance.timeoff_application_applicant, schedule_date=end_date)
                if check_schedule_qs.count() > 0:
                    validated_start_time = ''
                    validated_end_time = ''
                    if start_time > check_schedule_qs[0].schedule_work_shift.shift_start_time:
                        validated_start_time = start_time
                    else:
                        validated_start_time = check_schedule_qs[0].schedule_work_shift.shift_start_time
                    if end_time > check_schedule_qs[0].schedule_work_shift.shift_end_time:
                        validated_end_time = check_schedule_qs[0].schedule_work_shift.shift_end_time
                    else:
                        validated_end_time = end_time
                    # create the timeoff record
                    Timeoff.objects.create(timeoff_employee=new_instance.timeoff_application_applicant, timeoff_date=end_date, timeoff_start_time=validated_start_time, timeoff_end_time=validated_end_time, timeoff_type=new_instance.timeoff_application_type.timeoff_type_name)
            if end_date > start_date:
                date_range = [timezone.localdate(new_instance.timeoff_application_start_datetime) + timedelta(days=x)  for x in range(timeoff_days + 1)]
                check_schedule_qs = Schedule.objects.filter(schedule_employee=new_instance.timeoff_application_applicant, schedule_date__in=date_range).order_by('created_time')
                if check_schedule_qs.count() > 0:
                    timeoff_create_bluk_list = []
                    check_schedule_dict = dict(zip([x[0] for x in check_schedule_qs.values_list('schedule_date')], check_schedule_qs))
                    for index, d in enumerate(check_schedule_dict.keys()):
                        if index == 0:
                            validated_start_time = ''
                            validated_end_time = ''
                            if check_schedule_dict[d].schedule_work_shift.shift_start_time > start_time:
                                validated_start_time = check_schedule_dict[d].schedule_work_shift.shift_start_time
                                validated_end_time = check_schedule_dict[d].schedule_work_shift.shift_end_time
                            else:
                                validated_start_time = start_time
                                validated_end_time = check_schedule_dict[d].schedule_work_shift.shift_end_time
                            timeoff_create_bluk_list.append(Timeoff(timeoff_employee=new_instance.timeoff_application_applicant, timeoff_date=d, timeoff_start_time=validated_start_time, timeoff_end_time=validated_end_time, timeoff_type=new_instance.timeoff_application_type.timeoff_type_name))
                        elif index == len(check_schedule_dict.keys()) - 1:
                            validated_start_time = ''
                            validated_end_time = ''
                            if check_schedule_dict[d].schedule_work_shift.shift_end_time > end_time:
                                validated_end_time = end_time
                                validated_start_time = check_schedule_dict[d].schedule_work_shift.shift_start_time
                            else:
                                validated_end_time = check_schedule_dict[d].schedule_work_shift.shift_end_time
                                validated_start_time = check_schedule_dict[d].schedule_work_shift.shift_start_time
                            timeoff_create_bluk_list.append(Timeoff(timeoff_employee=new_instance.timeoff_application_applicant, timeoff_date=d, timeoff_start_time=validated_start_time, timeoff_end_time=validated_end_time, timeoff_type=new_instance.timeoff_application_type.timeoff_type_name))
                        else:
                            timeoff_create_bluk_list.append(Timeoff(timeoff_employee=new_instance.timeoff_application_applicant, timeoff_date=d, timeoff_start_time=check_schedule_dict[d].schedule_work_shift.shift_start_time, timeoff_end_time=check_schedule_dict[d].schedule_work_shift.shift_end_time, timeoff_type=new_instance.timeoff_application_type.timeoff_type_name))
                    Timeoff.objects.bulk_create(timeoff_create_bluk_list)
            if end_date < start_date:
                # front-end validate the start_datetime and end_datetime
                pass
            return new_instance


class TimeoffSerializer(serializers.ModelSerializer):
    timeoff_employee_hm = serializers.SerializerMethodField()
    timeoff_employee_dept_hm = serializers.SerializerMethodField()
    timeoff_start_datetime_hm = serializers.SerializerMethodField()
    timeoff_end_datetime_hm = serializers.SerializerMethodField()

    class Meta:
        model = Timeoff
        fields = '__all__'

    def get_timeoff_employee_hm(self, obj):
        res_name = f"{obj.timeoff_employee.employee.first_name.capitalize()} {obj.timeoff_employee.employee.last_name.capitalize()}"
        return res_name

    def get_timeoff_employee_dept_hm(self, obj):
        res_dept = obj.timeoff_employee.employee_department.department.name
        return res_dept

    def get_timeoff_start_datetime_hm(self, obj):
        return f"{obj.timeoff_date} {obj.timeoff_start_time}"

    def get_timeoff_end_datetime_hm(self, obj):
        return f"{obj.timeoff_date} {obj.timeoff_end_time}"


class TimeoffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeoffType
        fields = '__all__'


class SelectBoxTimeoffTypeSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="timeoff_type_name")
    class Meta:
        model = TimeoffType
        fields = ['id', 'value']