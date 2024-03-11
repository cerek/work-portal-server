import copy
from rest_framework.permissions import DjangoModelPermissions, BasePermission

class ViewMyTicketPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_ticket_personal']


class ViewMyDeptTicketPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_todo_ticket_dept']
        self.perms_map['PUT'] = ['%(app_label)s.update_ticket_department']
        self.perms_map['PATCH'] = ['%(app_label)s.update_ticket_department']