from rest_framework import serializers
from qms.models import QMSTicket, QMSServiceType, QMSTicketTemplate


class QMSServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QMSServiceType
        fields = '__all__'


class QMSTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = QMSTicket
        fields = '__all__'


class QMSTicketTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = QMSTicketTemplate
        fields = '__all__'