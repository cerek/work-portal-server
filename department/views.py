from rest_framework import viewsets, status
from rest_framework.response import Response
from department.models import Department
from department.serializers import DepartmentSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ['department__name',
                        'department_desc', 'department_status']
    search_fields = ['department__name',
                     'department_desc', 'department_status']
    pagination_class = StandardResultsSetPagination

    def destroy(self, request, *args, **kwargs):
        delete_obj = self.get_object()
        obj_serializer = self.get_serializer(self.get_object()).data

        # Using the delete() with Group object, the related Department object will be deleted
        if delete_obj.department:
            delete_obj.department.delete()

        # Return the deleted object to client.
        return Response(obj_serializer, status=status.HTTP_200_OK)
