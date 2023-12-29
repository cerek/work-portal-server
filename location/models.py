from django.db import models


class Location(models.Model):
    location_name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    location_address = models.CharField(max_length=300, null=True, blank=True)
    location_zipcode = models.CharField(max_length=10, null=True, blank=True)
    location_desc = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ['-id']