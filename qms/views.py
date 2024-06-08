from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from qms.models import QMSServiceType, QMSTicket, QMSTicketTemplate
from qms.serializers import QMSServiceTypeSerializer, QMSTicketSerializer, QMSTicketTemplateSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class QMSServiceTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = QMSServiceType.objects.all()
    serializer_class = QMSServiceTypeSerializer
    filterset_fields = {}
    search_fields = []
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


class QMSTicketViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = QMSTicket.objects.all()
    serializer_class = QMSTicketSerializer
    filterset_fields = {}
    search_fields = []
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


class QMSTicketTemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = QMSTicketTemplate.objects.all()
    serializer_class = QMSTicketTemplateSerializer
    filterset_fields = {}
    search_fields = []
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