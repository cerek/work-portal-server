import copy
from rest_framework.permissions import DjangoModelPermissions


class ViewPersonalSchedulePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_schedule_personal']


class ViewPersonalScheduleChangePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_schedule_change_personal']


class DecideScheduleChangePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['PATCH'] = ['%(app_label)s.manager_approval_schedule_change']