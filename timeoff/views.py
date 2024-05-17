from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from timeoff.models import TimeoffApplication, Timeoff, TimeoffType
from timeoff.serializers import TimeoffApplicationSerializer, TimeoffSerializer, MyTimeoffSerializer, TimeoffTypeSerializer, SelectBoxTimeoffTypeSerializer
from timeoff.permissions import ViewPersonalTimeoffPermission
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class TimeoffApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = TimeoffApplication.objects.all()
    serializer_class = TimeoffApplicationSerializer
    filterset_fields = {'timeoff_application_applicant': ['exact'], 'timeoff_application_applicant__employee__username': ['exact', 'icontains'], 'timeoff_application_applicant__employee_department__department__name': ['exact', 'icontains'], 
                        'timeoff_application_applicant__employee__email': ['exact', 'icontains'], 'timeoff_application_start_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_end_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_apply_reason': ['exact', 'icontains'], 'timeoff_application_reject_reason': ['exact', 'icontains']}
    search_fields = ['timeoff_application_applicant__employee__username', 'timeoff_application_applicant__employee_department__department__name', 'timeoff_application_applicant__employee__email', 'timeoff_application_apply_reason', 'timeoff_application_reject_reason']
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


class TimeoffViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Timeoff.objects.all()
    serializer_class = TimeoffSerializer
    filterset_fields = ['timeoff_apply_employee__employee__username', 'timeoff_approval_employee__employee__username', 'timeoff_status', 'timeoff_start_datetime', 'timeoff_end_datetime', 'timeoff_reason']
    search_fields = ['timeoff_apply_employee__employee__username', 'timeoff_approval_employee__employee__username', 'timeoff_status', 'timeoff_reason']
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


class MyTimeoffViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated & ViewPersonalTimeoffPermission]
    serializer_class = MyTimeoffSerializer
    filterset_fields = ['timeoff_apply_employee__employee__username', 'timeoff_approval_employee__employee__username', 'timeoff_status', 'timeoff_start_datetime', 'timeoff_end_datetime', 'timeoff_reason']
    search_fields = ['timeoff_apply_employee__employee__username', 'timeoff_approval_employee__employee__username', 'timeoff_status', 'timeoff_reason']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = Timeoff.objects.filter(timeoff_apply_employee=user.employee)
        return qs


class TimeoffTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = TimeoffType.objects.all()
    serializer_class = TimeoffTypeSerializer
    filterset_fields = ['timeoff_type_name']
    search_fields = ['timeoff_type_name']
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

class SelectBoxTimeoffTypeViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TimeoffType.objects.all()
    serializer_class = SelectBoxTimeoffTypeSerializer
    filterset_fields = ['timeoff_type_name']
    search_fields = ['timeoff_type_name']
    pagination_class = StandardResultsSetPagination