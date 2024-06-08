from rest_framework import serializers
from clocking.models import ClockingMachine
from clocking.models import ClockingRecord
from clocking.models import ClockingFingerRecord


class ClockingRecordSerializer(serializers.ModelSerializer):
    clocking_record_employee_name_hm = serializers.SerializerMethodField()
    clocking_record_employee_dept_hm = serializers.SerializerMethodField()
    clocking_record_is_edit_hm = serializers.SerializerMethodField()
    clocking_record_machine_name_hm = serializers.SerializerMethodField()
    clocking_record_machine_location_hm = serializers.SerializerMethodField()

    class Meta:
        model = ClockingRecord
        fields = '__all__'

    def get_clocking_record_employee_name_hm(self, obj):
        res_name = f"{obj.clocking_record_employee.employee.first_name.capitalize()} {obj.clocking_record_employee.employee.last_name.capitalize()}"
        return res_name

    def get_clocking_record_employee_dept_hm(self, obj):
        return obj.clocking_record_employee.employee_department.department.name

    def get_clocking_record_is_edit_hm(self, obj):
        return obj.get_clocking_record_is_edit_display()

    def get_clocking_record_machine_name_hm(self, obj):
        res_name = obj.clocking_record_machine.clocking_machine_name
        return res_name

    def get_clocking_record_machine_location_hm(self, obj):
        res_name = obj.clocking_record_machine.clocking_machine_location.location_name
        return res_name

    # def create(self, validated_data):
    #     import time
    #     time.sleep(20)
    #     return super().create(validated_data)


class ClockingMachineSerializer(serializers.ModelSerializer):
    clocking_machine_status_hm = serializers.SerializerMethodField()
    clocking_machine_location_hm = serializers.SerializerMethodField()
    clocking_machine_type_hm = serializers.SerializerMethodField()

    class Meta:
        model = ClockingMachine
        fields = '__all__'

    def get_clocking_machine_status_hm(self, obj):
        return obj.get_clocking_machine_status_display()

    def get_clocking_machine_location_hm(self, obj):
        res_name = obj.clocking_machine_location.location_name
        return res_name

    def get_clocking_machine_type_hm(self, obj):
        return obj.get_clocking_machine_type_display()


class ClockingFingerRecordSerializer(serializers.ModelSerializer):
    finger_record_employee_name_hm = serializers.SerializerMethodField()
    finger_record_employee_dept_hm = serializers.SerializerMethodField()
    finger_record_machine_name_hm = serializers.SerializerMethodField()
    finger_record_choose_hm = serializers.SerializerMethodField()

    class Meta:
        model = ClockingFingerRecord
        fields = '__all__'

    def get_finger_record_employee_name_hm(self, obj):
        res_name = f"{obj.finger_record_employee.employee.first_name.capitalize()} {obj.finger_record_employee.employee.last_name.capitalize()}"
        return res_name

    def get_finger_record_employee_dept_hm(self, obj):
        return obj.finger_record_employee.employee_department.department.name

    def get_finger_record_machine_name_hm(self, obj):
        machine_list = obj.finger_record_machine.all()
        res_list = [x.clocking_machine_name for x in machine_list]
        return res_list

    def get_finger_record_choose_hm(self, obj):
        return obj.get_finger_record_choose_display()


class SelectBoxClockingMachineSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = ClockingMachine
        fields = ['id', 'value']

    def get_value(self, obj):
        res_name = f'{obj.clocking_machine_name.capitalize()}'
        return res_name