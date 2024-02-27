# Generated by Django 3.2.20 on 2024-01-24 08:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timeoff', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeoff',
            options={'ordering': ['-created_time'], 'permissions': [('view_timeoff_approval', 'Can view timeoff approval list'), ('manager_approval_timeoff', 'Can approval the timeoff'), ('view_timeoff_all_report', 'Can view all timeoff report'), ('view_timeoff_own_report', 'Can only view own timeoff report')]},
        ),
        migrations.AddField(
            model_name='timeofftype',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeofftype',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]