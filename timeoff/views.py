from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from timeoff.models import TimeoffApplication, Timeoff, TimeoffType
from timeoff.serializers import TimeoffApplicationSerializer, TimeoffSerializer, TimeoffTypeSerializer, MyTimeoffApplicationSerializer, TimeoffApplicationDecideSerializer, SelectBoxTimeoffTypeSerializer
from timeoff.permissions import ViewPersonalTimeoffPermission, ViewPersonalTimeoffApplicationPermission, DecideTimeoffApplicationPermission
from employee.models import Employee
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class TimeoffApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = TimeoffApplication.objects.all()
    serializer_class = TimeoffApplicationSerializer
    filterset_fields = {'timeoff_application_applicant': ['exact'], 'timeoff_application_applicant__employee__username': ['exact', 'icontains'], 'timeoff_application_applicant__employee_department__department__name': ['exact', 'icontains'],
                        'timeoff_application_applicant__employee__email': ['exact', 'icontains'], 'timeoff_application_start_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_end_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_apply_reason': ['exact', 'icontains'], 'timeoff_application_reject_reason': ['exact', 'icontains']}
    search_fields = ['timeoff_application_applicant__employee__username', 'timeoff_application_applicant__employee_department__department__name',
                     'timeoff_application_applicant__employee__email', 'timeoff_application_apply_reason', 'timeoff_application_reject_reason']
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


class TimeoffApplicationDecideViewSet(UpdateAPIView):
    permission_classes = [DecideTimeoffApplicationPermission]
    serializer_class = TimeoffApplicationDecideSerializer
    queryset = TimeoffApplication.objects.all()


class TimeoffForEmployeeViewSet(ListAPIView):
    permission_classes = [ExtendViewPermission]
    serializer_class = TimeoffSerializer
    filterset_fields = {'timeoff_employee': ['exact'], 'timeoff_employee__employee__username': ['exact', 'icontains'], 'timeoff_employee__employee_department__department__name': [
        'icontains'], 'timeoff_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_start_time': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_end_time': ['exact', 'lt', 'gt', 'lte', 'gte']}
    search_fields = ['timeoff_employee', 'timeoff_employee__employee__username',
                     'timeoff_employee__employee_department__department__name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.parser_context['kwargs'].get('pk', '')
        timeoff_employee = Employee.objects.filter(pk=int(user))
        if timeoff_employee.exists():
            qs = Timeoff.objects.filter(
                timeoff_employee=timeoff_employee.last())
        else:
            qs = Timeoff.objects.none()
        return qs


class MyTimeoffApplicationViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [ViewPersonalTimeoffApplicationPermission]
    serializer_class = MyTimeoffApplicationSerializer
    filterset_fields = {'timeoff_application_applicant': ['exact'], 'timeoff_application_applicant__employee__username': ['exact', 'icontains'], 'timeoff_application_applicant__employee_department__department__name': ['exact', 'icontains'],
                        'timeoff_application_applicant__employee__email': ['exact', 'icontains'], 'timeoff_application_start_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_end_datetime': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_application_apply_reason': ['exact', 'icontains'], 'timeoff_application_reject_reason': ['exact', 'icontains']}
    search_fields = ['timeoff_application_applicant__employee__username', 'timeoff_application_applicant__employee_department__department__name',
                     'timeoff_application_applicant__employee__email', 'timeoff_application_apply_reason', 'timeoff_application_reject_reason']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = TimeoffApplication.objects.filter(
            timeoff_application_applicant=user.employee)
        return qs


class TimeoffViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Timeoff.objects.all()
    serializer_class = TimeoffSerializer
    filterset_fields = {'timeoff_employee': ['exact'], 'timeoff_employee__employee__username': ['exact', 'icontains'], 'timeoff_employee__employee_department__department__name': [
        'icontains'], 'timeoff_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_start_time': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_end_time': ['exact', 'lt', 'gt', 'lte', 'gte']}
    search_fields = ['timeoff_employee', 'timeoff_employee__employee__username',
                     'timeoff_employee__employee_department__department__name']
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


class MyTimeoffViewSet(ListAPIView):
    permission_classes = [ViewPersonalTimeoffPermission]
    serializer_class = TimeoffSerializer
    filterset_fields = {'timeoff_employee': ['exact'], 'timeoff_employee__employee__username': ['exact', 'icontains'], 'timeoff_employee__employee_department__department__name': [
        'icontains'], 'timeoff_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_start_time': ['exact', 'lt', 'gt', 'lte', 'gte'], 'timeoff_end_time': ['exact', 'lt', 'gt', 'lte', 'gte']}
    search_fields = ['timeoff_employee', 'timeoff_employee__employee__username',
                     'timeoff_employee__employee_department__department__name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = Timeoff.objects.filter(timeoff_employee=user.employee)
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
