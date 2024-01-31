import copy
from rest_framework.permissions import DjangoModelPermissions


class ViewPersonalTimeoffPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_timeoff_personal']