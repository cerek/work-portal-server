import copy
from rest_framework.permissions import DjangoModelPermissions, BasePermission

class ViewMyTicketPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_ticket_personal']