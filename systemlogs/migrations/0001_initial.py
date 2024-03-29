# Generated by Django 3.2.20 on 2024-03-17 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0004_alter_employee_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Systemlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systemlog_operate_module', models.CharField(max_length=200)),
                ('systemlog_request_method', models.SmallIntegerField(choices=[(0, 'GET'), (1, 'POST'), (2, 'PUT'), (3, 'PATCH'), (4, 'DELETE')])),
                ('systemlog_request_body', models.CharField(default='-', max_length=500)),
                ('systemlog_request_ip', models.GenericIPAddressField()),
                ('systemlog_request_agent', models.CharField(max_length=300)),
                ('systemlog_request_time', models.DateTimeField(auto_now_add=True)),
                ('systemlog_response_code', models.SmallIntegerField()),
                ('systemlog_response_context', models.TextField(default='-')),
                ('systemlog_operator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employee.employee')),
            ],
        ),
    ]
