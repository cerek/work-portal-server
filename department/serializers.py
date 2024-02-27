from django.contrib.auth.models import Group
from rest_framework import serializers
from department.models import Department


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    department = GroupSerializer()
    department_status_hm = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    # Show the choices with 'Hunman-readable' value
    def get_department_status_hm(self, obj):
        return obj.get_department_status_display()

    def create(self, validated_data):
        group_data = validated_data.pop('department', {})
        group_serializer = GroupSerializer(data=group_data)
        if group_serializer.is_valid():
            try:
                department = group_serializer.save()
                new_department = Department.objects.create(
                    department=department, **validated_data)
            except Exception as e:
                raise serializers.ValidationError({"error": e})
            return new_department

    def update(self, instance, validated_data):
        group_data = validated_data.pop('department', {})
        group_serializer = GroupSerializer(
            instance=instance.department, data=group_data)

        if group_serializer.is_valid():
            group_serializer.save()

        return super().update(instance, validated_data)

class SelectBoxDepartmentSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'value']

    def get_value(self, obj):
        res_department = f'{obj.department.name.capitalize()}'
        return res_department