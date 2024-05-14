from django.db import models
from employee.models import Employee
from workshift.models import WorkShift


class Schedule(models.Model):
    schedule_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    schedule_date = models.DateField()
    schedule_work_shift = models.ForeignKey(WorkShift, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.schedule_employee.employee.username}({self.schedule_date})"

    class Meta:
        ordering = ['-id']
        permissions = [
            ('view_schedule_personal', 'Can view schedule personal'),
        ]


class SchedulePlan(models.Model):
    STATUS_CHOICES = (
        (0, 'Suspend'),
        (1, 'Active'),
    )
    schedule_plan_name = models.CharField(max_length=200, blank=False, null=False)
    schedule_plan_employee = models.ManyToManyField(Employee, blank=True)
    schedule_plan_work_day = models.CharField(max_length=20) 
    schedule_plan_start_date = models.DateField()
    schedule_plan_end_date = models.DateField()
    schedule_plan_work_shift = models.ForeignKey(WorkShift, on_delete=models.DO_NOTHING)
    schedule_plan_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    schedule_plan_sync = models.BooleanField(default=False)
    schedule_plan_desc = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.schedule_plan_name}({self.schedule_plan_start_date} - {self.schedule_plan_end_date})"

    class Meta:
        ordering = ['-created_time']


class ScheduleChange(models.Model):
    TYPE_CHOICES = (
        (0, 'Short Term'),
        (1, 'Long Term'),
    )
    STATUS_CHOICES = (
        (0, 'New'),
        (1, 'Approval'),
        (2, 'Reject'),
        (3, 'Cancel'),
    )
    schedule_change_applicant = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='schedule_change_applicant')
    schedule_change_approver = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, related_name='schedule_change_approver')
    schedule_change_work_shift = models.ForeignKey(WorkShift, on_delete=models.DO_NOTHING)
    schedule_change_apply_reason = models.TextField(null=True, blank=True)
    schedule_change_reject_reason = models.TextField(null=True, blank=True)
    schedule_change_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0)
    schedule_change_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    schedule_change_start_date = models.DateField(null=True, blank=True)
    schedule_change_end_date = models.DateField(null=True, blank=True)
    schedule_change_work_day = models.CharField(max_length=50, null=True, blank=True)
    schedule_change_off_date = models.CharField(max_length=50, null=True, blank=True)
    schedule_change_work_date = models.CharField(max_length=50, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
        permissions = [
            ('view_schedule_change_approval', 'Can view schedule change approval list'),
            ('view_schedule_change_personal', 'Can view schedule change personal'),
            ('manager_approval_schedule_change', 'Can approval the schedule change'),
            ('view_schedule_change_all_report', 'Can view all schedule change report'),
            ('view_schedule_change_own_report', 'Can only view own schedule change report'),
        ]
