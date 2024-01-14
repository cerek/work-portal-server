# Generated by Django 3.2.20 on 2024-01-13 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_employee_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['-id'], 'permissions': [('view_employee_profile', 'Can view employee profile'), ('view_employee_dept_contact', 'Can view employee department contact'), ('view_employee_all_contact', 'Can view employee all contact'), ('change_employee_password', 'Can change employee password'), ('change_employee_permission', 'Can change employee permission'), ('change_department_permission', 'Can change department permission')]},
        ),
    ]
