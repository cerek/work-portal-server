# Generated by Django 3.2.20 on 2024-05-04 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_scheduleplan_schedule_plan_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleplan',
            name='schedule_plan_sync',
            field=models.BooleanField(default=False),
        ),
    ]