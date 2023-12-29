# Generated by Django 3.2.20 on 2023-12-27 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employee.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_num', models.PositiveSmallIntegerField(blank=True, null=True, unique=True)),
                ('employee_job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('employee_gender', models.SmallIntegerField(choices=[(0, 'Female'), (1, 'Male'), (10, 'Prefer Not to Answer.')], default=10)),
                ('employee_phone', models.CharField(blank=True, max_length=30, null=True)),
                ('employee_extension', models.CharField(blank=True, max_length=10, null=True)),
                ('employee_join_day', models.DateTimeField(blank=True, default=employee.models.get_today, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee_department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='department.department')),
                ('employee_work_location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='location.location')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': [('view_employee_profile', 'Can view employee profile'), ('view_employee_dept_contact', 'Can view employee department contact'), ('view_employee_all_contact', 'Can view employee all contact'), ('change_employee_password', 'Can change employee password')],
            },
        ),
    ]
