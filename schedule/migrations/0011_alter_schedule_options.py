# Generated by Django 3.2.20 on 2024-05-12 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_auto_20240510_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['-id'], 'permissions': [('view_schedule_personal', 'Can view schedule personal')]},
        ),
    ]
