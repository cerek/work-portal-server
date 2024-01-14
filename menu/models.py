from django.db import models
from django.contrib.auth.models import Permission


class Menu(models.Model):
    PRIORITY_CHOICES = [ (x, x) for x in range(1,10) ]
    TYPE_CHOICES = [
        (0, 'Public'),
        (1, 'Main'),
        (2, 'Level1'),
        (3, 'Level2'),
        (4, 'Level3'),
    ]
    STATUS_CHOICES = [
        (0, 'Suspend'),
        (1, 'Active'),
    ]
    CATEGORY_CHOICES = [
        (0, 'Public Menu'),
        (1, 'IT Menu'),
        (2, 'HR Menu'),
        (3, 'Accounting Menu'),
        (4, 'Inventory Menu'),
        (5, 'Sale Menu'),
        (10, 'Admin Menu'),
    ]
    NEED_ID_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    permission = models.OneToOneField(Permission, on_delete=models.DO_NOTHING, null=True, blank=True)
    menu_parent_id = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)
    menu_name = models.CharField(max_length=200, unique=True)
    menu_url = models.CharField(max_length=100, default='#')
    menu_show = models.CharField(max_length=100)
    menu_priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=1)
    menu_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0)
    menu_icon = models.CharField(max_length=100, null=True, blank=True, default="")
    menu_category = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=0)
    menu_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    menu_need_id = models.SmallIntegerField(choices=NEED_ID_CHOICES, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_show
    
    class Meta:
        ordering = ['-id']