from django.db import models
from datetime import datetime


def get_today(instance, filename):
    return datetime.now().strftime("%Y%m%d") + "/" + filename


class Upload(models.Model):
    file_name = models.CharField(max_length=30, null=True, blank=True)
    file_url = models.ImageField(
        upload_to=get_today, default='', null=True, blank=True)
    file_uploader = models.CharField(max_length=20, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.file_name
