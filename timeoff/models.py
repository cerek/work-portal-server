from django.db import models
from datetime import datetime
from employee.models import Employee


class Timeoff(models.Model):
    TIMEOFF_STATUS = [
        (1, 'Apply'),
        (2, 'Manager Approval'),
        (3, 'HR Approval'),
        (4, 'Cancel'),
    ]
    timeoff_apply_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='timeoff_apply_employee')
    timeoff_approval_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, related_name='timeoff_approval_employee')
    timeoff_type = models.ForeignKey('TimeoffType', on_delete=models.DO_NOTHING)
    timeoff_status = models.SmallIntegerField(choices=TIMEOFF_STATUS, default=1)
    timeoff_start_datetime = models.DateTimeField()
    timeoff_end_datetime = models.DateTimeField()
    timeoff_reason = models.TextField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def gain_timeoff_hours(self):
        # [Enhance] The calculate method should be follow the rules like below:
        # 1. More than 1 day timeoff, N * 8 + Minutes
        # 2. Less than 1 day timeoff, Minutes
        # 3. Deduct the lunch time or not
        timeoff_hours = self.timeoff_end_datetime - self.timeoff_start_datetime
        return "{:.2f}".format(timeoff_hours.total_seconds() / 60 / 60)

    class Meta:
        ordering = ['-created_time']
        permissions = [
            ('view_timeoff_approval', 'Can view timeoff approval list'),
            ('view_timeoff_personal', 'Can view timeoff personal'),
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
