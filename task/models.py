from django.db import models
from django_celery_beat.models import PeriodicTask
from employee.models import Employee


class WorkPeriodicTask(PeriodicTask):
    TASK_TYPE_CHOICES = [
        (0, 'OneTime Job'),
        (1, 'Cron Job'),
        (2, 'Interval Job'),
    ]
    task_creator = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=False, blank=False)
    task_type = models.SmallIntegerField(choices=TASK_TYPE_CHOICES, null=False, blank=False, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

# class TaskScript(models.Model):
#     task_script_name = models.CharField(max_length=200, null=False, blank=False)
#     task_script_path = models.CharField(max_length=300, null=False, blank=False)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)