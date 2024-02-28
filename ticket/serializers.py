from rest_framework import serializers
from ticket.models import Ticket, TicketType


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
        res_list = [{'id': x.id, 'attachment_name': x.file_name,
                     'attachment_url': x.file_url.url} for x in all_attachments]
        return res_list


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class MyTicketSerializer(TicketSerializer):
    ticket_creator = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        # Prevent submit with ticket_creator, ticket_assigner, ticket_solution, ticket_status
        for deny_field in ['ticket_creator', 'ticket_assigner', 'ticket_solution', 'ticket_status', 'ticket_final_time']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError(
                    {deny_field: f"Can't submit with {deny_field}"})

        new_ticket_attachments = []
        if 'ticket_attachment' in validated_data:
            new_ticket_attachments = validated_data.pop('ticket_attachment')

        new_ticket = Ticket.objects.create(
            ticket_creator=user.employee, ticket_status=0, **validated_data)
        new_ticket.ticket_attachment.set(new_ticket_attachments)
        return new_ticket

    def update(self, instance, validated_data):
        # Only can edit the ticket_title, ticket_assign_department, ticket_description, ticket_type, ticket_attachment when the ticket status is new
        for deny_field in ['ticket_creator', 'ticket_assigner', 'ticket_solution', 'ticket_final_time']:
            if deny_field in validated_data.keys():
                raise serializers.ValidationError(
                    {deny_field: f"Can't update with {deny_field}"})
        if 'ticket_status' in validated_data.keys():
            if validated_data['ticket_status'] != 5:
                raise serializers.ValidationError(
                    {'ticket_status': 'You can\'t change the ticket status except "Close".'})
        if instance.ticket_status == 5:
            raise serializers.ValidationError(
                {'ticket_status': 'You can\'t edit a "Close" Ticket. Please create a new Ticket to report your issue.'})
        else:
            return super().update(instance, validated_data)


class SelectBoxTicketTypeSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="ticket_type_name")
    class Meta:
        model = TicketType
        fields = ['id', 'value']
