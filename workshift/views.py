from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from workshift.models import WorkShift
from workshift.serializers import WorkShiftSerializer, SelectBoxWorkShiftSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class WorkShiftViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    filterset_fields = ['shift_name',
                        'shift_start_time', 'shift_end_time', 'shift_status']
    search_fields = ['shift_name',
                     'shift_start_time', 'shift_end_time', 'shift_status']
    pagination_class = StandardResultsSetPagination

    def destroy(self, request, *args, **kwargs):
        delete_obj = self.get_object()
        obj_serializer = self.get_serializer(self.get_object()).data

        try:
            delete_obj.delete()
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        # Return the deleted object to client.
        return Response(obj_serializer, status=status.HTTP_200_OK)


class SelectBoxWorkShiftViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectBoxWorkShiftSerializer
    queryset = WorkShift.objects.all()
    filterset_fields = ['shift_name',
                        'shift_start_time', 'shift_end_time', 'shift_status']
    search_fields = ['shift_name',
                     'shift_start_time', 'shift_end_time', 'shift_status']
    pagination_class = StandardResultsSetPagination
