from django.db import models
from location.models import Location


class QMSTicket(models.Model):
    qms_ticket_number = models.SmallIntegerField()
    qms_ticket_service = models.ForeignKey('QMSServiceType', on_delete=models.DO_NOTHING)
    qms_ticket_template = models.ForeignKey('QMSTicketTemplate', on_delete=models.DO_NOTHING)
    qms_ticket_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']


class QMSServiceType(models.Model):
    PRIORITY_CHOICES = [ (x, x) for x in range(1,10) ]
    STATUS_CHOICES = [
        (0, 'Suspend'),
        (1, 'Active'),
    ]
    qms_service_type_parent_id = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)
    qms_service_type_name = models.CharField(max_length=200, unique=True)
    qms_service_type_priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=1)
    qms_service_type_icon = models.CharField(max_length=100, null=True, blank=True, default="")
    qms_service_type_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.qms_service_type_name}"

    class Meta:
        ordering = ['-id']


class QMSTicketTemplate(models.Model):
    qms_ticket_template_name = models.CharField(max_length=200, unique=True)
    qms_ticket_template_id = models.CharField(max_length=200, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']