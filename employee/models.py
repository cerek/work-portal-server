from django.db import models
from django.contrib.auth.models import User, Permission
from datetime import datetime
from location.models import Location
from department.models import Department


def get_today():
    return datetime.now()


class Employee(models.Model):
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
        (10, 'Prefer Not to Answer.'),
    ]

    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_num = models.PositiveSmallIntegerField(
        unique=True, null=True, blank=True)
    employee_job_title = models.CharField(max_length=50, null=True, blank=True)
    employee_gender = models.SmallIntegerField(
        choices=GENDER_CHOICES, default=10)
    employee_phone = models.CharField(max_length=30, null=True, blank=True)
    employee_extension = models.CharField(max_length=10, null=True, blank=True)
    employee_work_location = models.ForeignKey(
        Location, on_delete=models.DO_NOTHING)
    employee_department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING)
    employee_join_day = models.DateTimeField(
        default=get_today, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def calculate_day_onboard(self):
        # calculate the days of employee on board
        now_day = datetime.now()
        onboard_day = now_day - self.employee_join_day.replace(tzinfo=None)
        return onboard_day.days

    def gain_permission(self, type='all'):
        ret_list = []
        user_perm_codename_list = [
            x.split('.')[-1] for x in list(self.employee.get_user_permissions())]
        user_perm_qs = Permission.objects.filter(
            codename__in=user_perm_codename_list)
        group_perm_qs = self.employee_department.department.permissions.all()

        if type == 'user':
            ret_list = list(user_perm_qs.values_list('id', flat=True))
        elif type == 'group':
            ret_list = list(group_perm_qs.values_list('id', flat=True))
        else:
            all_perm_qs = user_perm_qs.union(group_perm_qs)
            ret_list = list(all_perm_qs.values_list('id', flat=True))
        return ret_list

    def __str__(self):
        return self.employee.username

    class Meta:
        ordering = ['-id']
        permissions = [
            ('view_employee_profile', 'Can view employee profile'),
            ('view_employee_dept_contact', 'Can view employee department contact'),
            ('view_employee_all_contact', 'Can view employee all contact'),
            ('change_employee_password', 'Can change employee password'),
        ]
