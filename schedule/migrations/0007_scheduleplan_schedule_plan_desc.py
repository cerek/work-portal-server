# Generated by Django 3.2.20 on 2024-04-30 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_scheduleplan_schedule_plan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleplan',
            name='schedule_plan_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
