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
    schedule_plan_desc = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.schedule_plan_name}({self.schedule_plan_start_date} - {self.schedule_plan_end_date})"

    class Meta:
        ordering = ['-created_time']
