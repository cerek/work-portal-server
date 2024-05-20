import copy
from rest_framework.permissions import DjangoModelPermissions


class ViewPersonalTimeoffPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_timeoff_personal']


class ViewPersonalTimeoffApplicationPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_timeoff_application_personal']


class DecideTimeoffApplicationPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['PATCH'] = ['%(app_label)s.manager_approval_timeoff']