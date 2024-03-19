from django.db import models
from employee.models import Employee


class Systemlogs(models.Model):
    REQUEST_METHOD_CHOICES = [
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'PATCH'),
        (4, 'DELETE'),
    ]
    systemlog_operator = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=False, blank=False)
    systemlog_operate_module = models.CharField(max_length=200, null=False, blank=False)
    systemlog_request_method = models.SmallIntegerField(choices=REQUEST_METHOD_CHOICES, null=False, blank=False)
    systemlog_request_body = models.TextField(null=False, blank=False, default='-')
    systemlog_request_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    systemlog_request_agent = models.CharField(max_length=300, null=False, blank=False)
    systemlog_request_time = models.DateTimeField(auto_now_add=True)
    systemlog_response_code = models.SmallIntegerField(null=False, blank=False)
    systemlog_response_duration = models.FloatField(null=False, blank=False)
    systemlog_response_context = models.TextField(null=False, blank=False, default='-')

    class Meta:
        ordering = ['-systemlog_request_time']