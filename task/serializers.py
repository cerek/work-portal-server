from rest_framework import serializers
from django_celery_beat.models import IntervalSchedule, ClockedSchedule, CrontabSchedule
from task.models import WorkPeriodicTask


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'


class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        exclude = ['timezone']


class WorkPeriodicTaskSerializer(serializers.ModelSerializer):
    task_creator_hm = serializers.SerializerMethodField()
    task_type_hm = serializers.SerializerMethodField()
    interval_hm = serializers.SerializerMethodField()
    clocked_hm = serializers.SerializerMethodField()
    crontab_hm = serializers.SerializerMethodField()
    period_data = serializers.JSONField(required=False, write_only=True, default={})
    task_creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkPeriodicTask
        fields = '__all__'

    def get_task_creator_hm(self, obj):
        return obj.task_creator.employee.username

    def get_task_type_hm(self, obj):
        return obj.get_task_type_display()

    def get_clocked_hm(self, obj):
        return obj.clocked.__str__()

    def get_crontab_hm(self, obj):
        return obj.crontab.__str__()

    def get_interval_hm(self, obj):
        return obj.interval.__str__()

    def create(self, validated_data):
        user = self.context['request'].user
        period_dict = {
            0: {"model": ClockedSchedule, "serializer": ClockedScheduleSerializer},
            1: {"model": CrontabSchedule, "serializer": CrontabScheduleSerializer},
            2: {"model": IntervalSchedule, "serializer": IntervalScheduleSerializer},
        }
        period_data = validated_data.pop('period_data', None)
        period_serializer = period_dict[validated_data['task_type']]['serializer'](data=period_data)
        if period_serializer.is_valid():
            # Only ClockedSchedule model have vaildators
            try:
                new_period, _ = period_dict[validated_data['task_type']]['model'].objects.get_or_create(**period_serializer.validated_data)
            except Exception as e:
                raise serializers.ValidationError({"error": e.args})
            period_validated_data = {
                0: {"one_off": True, "clocked": new_period, "crontab": None, "interval": None},
                1: {"one_off": False, "clocked": None, "crontab": new_period, "interval": None},
                2: {"one_off": False, "clocked": None, "crontab": None, "interval": new_period},
            }
            new_task = WorkPeriodicTask.objects.create(**validated_data, **period_validated_data[validated_data['task_type']], task_creator=user.employee)
            return new_task
        else:
            raise serializers.ValidationError({"error": period_serializer.errors})

    def update(self, instance, validated_data):
        period_dict = {
            0: {"model": ClockedSchedule, "serializer": ClockedScheduleSerializer},
            1: {"model": CrontabSchedule, "serializer": CrontabScheduleSerializer},
            2: {"model": IntervalSchedule, "serializer": IntervalScheduleSerializer},
        }
        if 'period_data' in validated_data:
            new_period_data = validated_data.pop('period_data', None)
            period_serializer = period_dict[validated_data['task_type']]['serializer'](data=new_period_data)
            if period_serializer.is_valid():
                # Only ClockedSchedule model have vaildators
                try:
                    new_period, _ = period_dict[validated_data['task_type']]['model'].objects.get_or_create(**period_serializer.validated_data)
                except Exception as e:
                    raise serializers.ValidationError({"error": e.args})
                period_validated_data = {
                    0: {"one_off": True, "clocked": new_period, "crontab": None, "interval": None},
                    1: {"one_off": False, "clocked": None, "crontab": new_period, "interval": None},
                    2: {"one_off": False, "clocked": None, "crontab": None, "interval": new_period},
                }
                validated_data.update(period_validated_data[validated_data['task_type']])
                return super().update(instance, validated_data)
        else:
            return super().update(instance, validated_data)


class SelectBoxClockedSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = ClockedSchedule
        fields = ['id', 'value']

    def get_value(self, obj):
        res_clocked = f'{obj.clocked_time}'
        return res_clocked


class SelectBoxCrontabSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = CrontabSchedule
        fields = ['id', 'value']

    def cronexp(self, field):
        return field and str(field).replace(' ', '') or '*'

    def get_value(self, obj):
        res_crontab = '{} {} {} {} {} (m/h/dM/MY/d) {}'.format(
            self.cronexp(obj.minute), self.cronexp(obj.hour),
            self.cronexp(obj.day_of_month), self.cronexp(obj.month_of_year),
            self.cronexp(obj.day_of_week), str(obj.timezone)
        )
        return res_crontab


class SelectBoxIntervalSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = IntervalSchedule
        fields = ['id', 'value']

    def get_value(self, obj):
        res_interval = f'every {obj.every} {obj.period}'
        return res_interval