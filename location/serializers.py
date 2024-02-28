from rest_framework import serializers
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SelectBoxLocationSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="location_name")

    class Meta:
        model = Location
        fields = ['id', 'value']