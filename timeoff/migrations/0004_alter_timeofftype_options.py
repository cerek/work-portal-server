# Generated by Django 3.2.20 on 2024-02-02 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeoff', '0003_alter_timeoff_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeofftype',
            options={'ordering': ['-created_time']},
        ),
    ]
