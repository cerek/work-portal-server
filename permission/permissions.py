import copy
from rest_framework.permissions import DjangoModelPermissions


class ViewEmployeePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['employee.view_employee_permission']

class ChangeEmployeePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['PUT'] = ['employee.view_employee_permission']


class ViewDepartmentPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['employee.view_department_permission']
