from rest_framework import serializers
from django.contrib.auth.models import Permission
from menu.models import Menu


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False)
    menu_type_hm = serializers.SerializerMethodField()
    menu_category_hm = serializers.SerializerMethodField()
    menu_status_hm = serializers.SerializerMethodField()
    menu_need_id_hm = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_menu_type_hm(self, obj):
        return obj.get_menu_type_display()

    def get_menu_category_hm(self, obj):
        return obj.get_menu_category_display()
    
    def get_menu_status_hm(self, obj):
        return obj.get_menu_status_display()

    def get_menu_need_id_hm(self, obj):
        return obj.get_menu_need_id_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Serialzier the permission information fromPrimaryKeyRelatedField
        if ret['permission'] is not None:
            permission_serializer = PermissionSerializer(Permission.objects.get(pk=ret['permission']))
            ret['permission'] = permission_serializer.data

        return ret