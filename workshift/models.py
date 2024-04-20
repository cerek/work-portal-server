from django.db import models


class WorkShift(models.Model):
    WORK_SHIFT_STATUS = [
        (0, 'Suspend'),
        (1, 'Active'),
    ]
    shift_name = models.CharField(max_length=200)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()
    shift_status = models.SmallIntegerField(choices=WORK_SHIFT_STATUS, default=1)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.shift_name} ({self.shift_start_time} - {self.shift_end_time})"
