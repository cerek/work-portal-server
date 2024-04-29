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