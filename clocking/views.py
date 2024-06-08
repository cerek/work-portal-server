from django.utils import timezone
from rest_framework import viewsets, status, mixins
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from clocking.models import ClockingMachine
from clocking.models import ClockingRecord
from clocking.models import ClockingFingerRecord
from clocking.serializers import ClockingMachineSerializer
from clocking.serializers import ClockingRecordSerializer
from clocking.serializers import ClockingFingerRecordSerializer
from clocking.serializers import SelectBoxClockingMachineSerializer
from clocking.permissions import ViewPersonalTimecardPermission
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class ClockingRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = ClockingRecordSerializer
    queryset = ClockingRecord.objects.all()
    filterset_fields = {'clocking_record_employee': ['exact'], 'clocking_record_employee__employee__username': ['exact', 'icontains'], 'clocking_record_employee__employee__email': ['exact', 'icontains'], 'clocking_record_employee__employee_department__department__name': ['exact', 'icontains'], 'clocking_record_datetime':['exact', 'lt', 'gt', 'lte', 'gte'], 'clocking_record_is_edit': ['exact'], 'clocking_record_machine__clocking_machine_name': ['exact', 'icontains'], 'clocking_record_machine__clocking_machine_location__location_name': ['exact', 'icontains']}
    search_fields = ['clocking_record_employee__employee__username', 'clocking_record_employee__employee__email', 'clocking_record_employee__employee_department__department__name', 'clocking_record_datetime', 'clocking_record_machine__clocking_machine_name', 'clocking_record_machine__clocking_machine_location__location_name']
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


class ClockingMachineViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = ClockingMachineSerializer
    queryset = ClockingMachine.objects.all()
    filterset_fields = {'clocking_machine_name': ['exact', 'icontains'], 'clocking_machine_status': ['exact'], 'clocking_machine_location__location_name': ['exact', 'icontains'], 'clocking_machine_type': ['exact'], 'clocking_machine_firmware_version': ['exact']}
    search_fields = ['clocking_machine_name', 'clocking_machine_location__location_name', 'clocking_machine_firmware_version', 'clocking_machine_desc']
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


class FingerRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = ClockingFingerRecordSerializer
    queryset = ClockingFingerRecord.objects.all()
    filterset_fields = {'finger_record_employee': ['exact'], 'finger_record_employee__employee__username': ['exact', 'icontains'], 'finger_record_employee__employee__email': ['exact', 'icontains'], 'finger_record_employee__employee_department__department__name': ['exact', 'icontains'], 'finger_record_machine__clocking_machine_name': ['exact', 'icontains'], 'finger_record_position': ['exact']}
    search_fields = ['finger_record_employee__employee__username', 'finger_record_employee__employee__email', 'finger_record_employee__employee_department__department__name', 'finger_record_machine__clocking_machine_name', 'finger_record_position']
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


class TimecardForEmployeeListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filterset_fields = {'clocking_record_employee': ['exact'], 'clocking_record_employee__employee__username': ['exact', 'icontains'], 'clocking_record_employee__employee__email': ['exact', 'icontains'], 'clocking_record_employee__employee_department__department__name': ['exact', 'icontains'], 'clocking_record_datetime':['exact', 'lt', 'gt', 'lte', 'gte'], 'clocking_record_is_edit': ['exact'], 'clocking_record_machine__clocking_machine_name': ['exact', 'icontains'], 'clocking_record_machine__clocking_machine_location__location_name': ['exact', 'icontains']}

    def list(self, request, *args, **kwargs):
        now_day = timezone.localdate()
        prior_date = now_day - timedelta(days=60)
        emp_id = request.parser_context['kwargs'].get('pk', '')
        start_date = request.query_params.get('clocking_record_datetime__gte', prior_date)
        end_date = request.query_params.get('clocking_record_datetime__lte', now_day)

        clocking_record_qs = ClockingRecord.objects.filter(clocking_record_employee=emp_id, clocking_record_datetime__date__gte=start_date, clocking_record_datetime__date__lte=end_date).order_by('clocking_record_datetime')

        tmp_list = []
        day_range = now_day - prior_date
        for d in range(day_range.days + 1):
            filter_day = prior_date + timedelta(days=d)
            filter_qs = clocking_record_qs.filter(clocking_record_datetime__date=filter_day.strftime("%Y-%m-%d"))
            tmp_list.append((filter_qs.first(), filter_qs.last()))

        res_dict = {}
        result_list = []
        for i in tmp_list:
            if i == (None, None):
                continue
            else:
                tmp_dict = {
                    "id": i[1].id,
                    "clocking_record_employee_name_hm": i[1].clocking_record_employee.employee.username,
                    "clocking_record_employee_dept_hm": i[1].clocking_record_employee.employee_department.department.name,
                    "clocking_record_date": i[1].clocking_record_datetime.astimezone().strftime('%Y-%m-%d'),
                    "clocking_record_first_time": i[0].clocking_record_datetime.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                    "clocking_record_last_time":i[1].clocking_record_datetime.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                }
                result_list.append(tmp_dict)
        res_dict['count'] = len(result_list)
        res_dict['results'] = result_list

        return Response(res_dict)


class MyTimecardListView(ListAPIView):
    permission_classes = [ViewPersonalTimecardPermission]
    serializer_class = ClockingRecordSerializer
    queryset = ClockingRecord.objects.all()
    filterset_fields = {'clocking_record_employee': ['exact'], 'clocking_record_employee__employee__username': ['exact', 'icontains'], 'clocking_record_employee__employee__email': ['exact', 'icontains'], 'clocking_record_employee__employee_department__department__name': ['exact', 'icontains'], 'clocking_record_datetime':['exact', 'lt', 'gt', 'lte', 'gte'], 'clocking_record_is_edit': ['exact'], 'clocking_record_machine__clocking_machine_name': ['exact', 'icontains'], 'clocking_record_machine__clocking_machine_location__location_name': ['exact', 'icontains']}
    search_fields = ['clocking_record_employee__employee__username', 'clocking_record_employee__employee__email', 'clocking_record_employee__employee_department__department__name', 'clocking_record_datetime', 'clocking_record_machine__clocking_machine_name', 'clocking_record_machine__clocking_machine_location__location_name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = ClockingRecord.objects.filter(clocking_record_employee=user.employee)
        return qs


class MyTimeCardForCalendarListView(ListAPIView):
    permission_classes = [ViewPersonalTimecardPermission]
    filterset_fields = {'clocking_record_employee': ['exact'], 'clocking_record_employee__employee__username': ['exact', 'icontains'], 'clocking_record_employee__employee__email': ['exact', 'icontains'], 'clocking_record_employee__employee_department__department__name': ['exact', 'icontains'], 'clocking_record_datetime':['exact', 'lt', 'gt', 'lte', 'gte'], 'clocking_record_is_edit': ['exact'], 'clocking_record_machine__clocking_machine_name': ['exact', 'icontains'], 'clocking_record_machine__clocking_machine_location__location_name': ['exact', 'icontains']}
    queryset = ClockingRecord.objects.all()
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        now_day = timezone.localdate()
        prior_date = now_day - timedelta(days=60)
        emp_id = request.user.employee.id
        start_date = request.query_params.get('clocking_record_datetime__gte', prior_date)
        end_date = request.query_params.get('clocking_record_datetime__lte', now_day)

        clocking_record_qs = ClockingRecord.objects.filter(clocking_record_employee=emp_id, clocking_record_datetime__date__gte=start_date, clocking_record_datetime__date__lte=end_date).order_by('clocking_record_datetime')

        tmp_list = []
        day_range = now_day - prior_date
        for d in range(day_range.days + 1):
            filter_day = prior_date + timedelta(days=d)
            filter_qs = clocking_record_qs.filter(clocking_record_datetime__date=filter_day.strftime("%Y-%m-%d"))
            tmp_list.append((filter_qs.first(), filter_qs.last()))

        res_dict = {}
        result_list = []
        for i in tmp_list:
            if i == (None, None):
                continue
            else:
                tmp_dict = {
                    "id": i[1].id,
                    "clocking_record_employee_name_hm": i[1].clocking_record_employee.employee.username,
                    "clocking_record_employee_dept_hm": i[1].clocking_record_employee.employee_department.department.name,
                    "clocking_record_date": i[1].clocking_record_datetime.astimezone().strftime('%Y-%m-%d'),
                    "clocking_record_first_time": i[0].clocking_record_datetime.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                    "clocking_record_last_time":i[1].clocking_record_datetime.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                }
                result_list.append(tmp_dict)
        res_dict['count'] = len(result_list)
        res_dict['results'] = result_list

        return Response(res_dict)


class SelectBoxClockingMachineViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectBoxClockingMachineSerializer
    queryset = ClockingMachine.objects.all()
    filterset_fields = {'clocking_machine_name': ['exact', 'icontains'], 'clocking_machine_status': ['exact'], 'clocking_machine_location__location_name': ['exact', 'icontains'], 'clocking_machine_type': ['exact'], 'clocking_machine_firmware_version': ['exact']}
    search_fields = ['clocking_machine_name', 'clocking_machine_location__location_name', 'clocking_machine_firmware_version', 'clocking_machine_desc']
    pagination_class = StandardResultsSetPagination