from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from location.models import Location
from location.serializers import LocationSerializer, SelectBoxLocationSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination

class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ['location_name', 'location_address', 'location_zipcode', 'location_desc']
    search_fields = ['location_name', 'location_address', 'location_zipcode', 'location_desc']
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


class SelectBoxLocationViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = SelectBoxLocationSerializer
    filterset_fields = ['location_name', 'location_address', 'location_zipcode', 'location_desc']
    search_fields = ['location_name', 'location_address', 'location_zipcode', 'location_desc']
    pagination_class = StandardResultsSetPagination