from django.db import models
from datetime import datetime
from employee.models import Employee


class TimeoffApplication(models.Model):
    TIMEOFFAPPLICATION_STATUS = [
        (1, 'Apply'),
        (2, 'Manager Approval'),
        (3, 'HR Approval'),
        (4, 'Cancel'),
        (5, 'Reject'),
    ]
    timeoff_application_applicant = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='timeoff_applicant')
    timeoff_application_approver = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, related_name='timeoff_approver')
    timeoff_application_type = models.ForeignKey('TimeoffType', on_delete=models.DO_NOTHING)
    timeoff_application_status = models.SmallIntegerField(choices=TIMEOFFAPPLICATION_STATUS, default=1)
    timeoff_application_start_datetime = models.DateTimeField()
    timeoff_application_end_datetime = models.DateTimeField()
    timeoff_application_apply_reason = models.TextField(max_length=500)
    timeoff_application_reject_reason = models.TextField(max_length=500, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
        permissions = [
            ('view_timeoff_application_approval', 'Can view timeoff application approval list'),
            ('view_timeoff_application_personal', 'Can view timeoff application personal'),
            ('manager_approval_timeoff', 'Can approval the timeoff'),
            ('view_timeoff_all_report', 'Can view all timeoff report'),
            ('view_timeoff_own_report', 'Can only view own timeoff report'),
        ]


class TimeoffType(models.Model):
    timeoff_type_name = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.timeoff_type_name

    class Meta:
        ordering = ['-created_time']
