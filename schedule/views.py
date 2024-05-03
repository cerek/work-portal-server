from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from schedule.models import Schedule, SchedulePlan
from schedule.serializers import ScheduleSerializer, SchedulePlanSerializer
from employee.models import Employee
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class ScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    filterset_fields = {'schedule_employee': ['exact'], "schedule_employee__employee__username": ['exact', 'icontains'],
                        'schedule_employee__employee__email': ['exact', 'icontains'], 'schedule_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'schedule_work_shift__shift_name': ['exact', 'icontains']}
    search_fields = ['schedule_employee__employee__username',
                     'schedule_employee__employee__email', 'schedule_date', 'schedule_work_shift__shift_name']
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


class ScheduleForEmployeeViewSet(ListAPIView):
    permission_classes = [ExtendViewPermission]
    serializer_class = ScheduleSerializer
    filterset_fields = {'schedule_employee': ['exact'], "schedule_employee__employee__username": ['exact', 'icontains'],
                        'schedule_employee__employee__email': ['exact', 'icontains'], 'schedule_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'schedule_work_shift__shift_name': ['exact', 'icontains']}
    search_fields = ['schedule_employee__employee__username',
                     'schedule_employee__employee__email', 'schedule_date', 'schedule_work_shift__shift_name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.parser_context['kwargs'].get('pk', '')
        schedule_employee = Employee.objects.filter(pk=int(user))
        if schedule_employee.exists():
            qs = Schedule.objects.filter(
                schedule_employee=schedule_employee.last())
        else:
            qs = Schedule.objects.none()
        return qs


class SchedulePlanViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = SchedulePlanSerializer
    queryset = SchedulePlan.objects.all()
    filterset_fields = {'schedule_plan_employee': ['exact'], "schedule_plan_employee__employee__username": ['exact', 'icontains'], 'schedule_plan_employee__employee__email': [
        'exact', 'icontains'], 'schedule_plan_start_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'schedule_plan_end_date': ['exact', 'lt', 'gt', 'lte', 'gte'], 'schedule_plan_work_shift__shift_name': ['exact', 'icontains']}
    search_fields = ['schedule_plan_employee__employee__username',
                     'schedule_plan_employee__employee__email', 'schedule_plan_start_date', 'schedule_plan_end_date', 'schedule_plan_work_shift__shift_name']
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
