from rest_framework import serializers
from ticket.models import Ticket, TicketType
from department.models import Department
from upload.models import Upload
from upload.serializers import UploadSerializer


class TicketSerializer(serializers.ModelSerializer):
    ticket_creator_hm = serializers.SerializerMethodField()
    ticket_creator_department_hm = serializers.SerializerMethodField()
    ticket_assigner_hm = serializers.SerializerMethodField()
    ticket_status_hm = serializers.SerializerMethodField()
    ticket_type_hm = serializers.SerializerMethodField()
    ticket_assign_department_hm = serializers.SerializerMethodField()
    ticket_attachment_hm = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_ticket_creator_hm(self, obj):
        return obj.ticket_creator.employee.username
    
    def get_ticket_creator_department_hm(self, obj):
        return obj.ticket_creator.employee_department.department.name

    def get_ticket_assigner_hm(self, obj):
        if obj.ticket_assigner:
            return obj.ticket_assigner.employee.username
        else:
            return '-'

    def get_ticket_assign_department_hm(self, obj):
        return obj.ticket_assign_department.department.name

    def get_ticket_type_hm(self, obj):
        return obj.ticket_type.ticket_type_name

    def get_ticket_status_hm(self, obj):
        return obj.get_ticket_status_display()

    def get_ticket_attachment_hm(self, obj):
        all_attachments = obj.ticket_attachment.all()
        res_list = [{'id': x.id, 'attachment_name': x.file_name, 'attachment_url': x.file_url.url} for x in all_attachments]
        return res_list


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class MyTicketSerializer(serializers.ModelSerializer):
    ticket_attachment = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.all(), required=False)
    class Meta:
        model = Ticket
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['ticket_status'] = dict(Ticket.STATUS_CHOICES).get(int(ret['ticket_status']))
        # Serialzier the Upload information fromPrimaryKeyRelatedField
        if ret['ticket_attachment'] is not None:
            attachment_serializer = UploadSerializer(Upload.objects.get(pk=ret['ticket_attachment']))
            ret['ticket_attachment'] = attachment_serializer.data
            # ret['ticket_attachment']['file_url'] = settings.BACKEND_URL + ret['ticket_attachment']['file_url']
        return ret

    def create(self, validated_data):
        user = self.context['request'].user
        # Prevent submit with ticket_creator_name and ticket_creator_dept
        for deny_field in ['ticket_creator_name', 'ticket_creator_dept', 'ticket_assigner_name']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't submit with {deny_field}"})
 
        new_ticket = Ticket.objects.create(ticket_creator_name=user.username, ticket_creator=user.employee, ticket_creator_dept=user.employee.employee_department.department.name, ticket_status=0, **validated_data)
        return new_ticket

    def update(self, instance, validated_data):
        # Prevent submit with ticket_creator_name and ticket_creator_dept
        for deny_field in ['ticket_creator', 'ticket_creator_name', 'ticket_creator_dept', 'ticket_assigner_name', 'ticket_solution', 'ticket_assigner']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError({deny_field: f"Can't update with {deny_field}"})
        if 'ticket_status' in validated_data.keys():
            if validated_data['ticket_status'] not in [0,5]:
                raise serializers.ValidationError({'ticket_status': 'Wrong ticket status updated!!!'})
        return super().update(instance, validated_data)