from django.db import models
from django.contrib.auth.models import Group


class Department(models.Model):
    STATUS_CHOICES = (
        (0, 'Suspend'),
        (1, 'Active'),
    )
    department = models.OneToOneField(Group, on_delete=models.CASCADE)
    department_desc = models.TextField(max_length=250, null=True, blank=True)
    department_status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=1)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department.name

    class Meta:
        ordering = ['-id']
