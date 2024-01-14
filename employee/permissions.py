import copy
from rest_framework.permissions import DjangoModelPermissions, BasePermission


class ViewProfile(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_employee_profile']

    def has_object_permission(self, request, view, obj):
        return obj == request.user.employee


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj == request.user.employee


class ViewContactPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_employee_dept_contact']


class ChangePasswordAdminPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['PUT'] = ['%(app_label)s.change_employee_password']