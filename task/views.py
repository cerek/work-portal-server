from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from task.models import WorkPeriodicTask
from task.serializers import WorkPeriodicTaskSerializer, WorkPeriodicTaskResultSerializer, ClockedScheduleSerializer, IntervalScheduleSerializer, CrontabScheduleSerializer
from task.serializers import SelectBoxClockedSerializer, SelectBoxCrontabSerializer, SelectBoxIntervalSerializer
from django_celery_beat.models import ClockedSchedule, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class WorkPeriodicTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = WorkPeriodicTask.objects.all()
    serializer_class = WorkPeriodicTaskSerializer
    filterset_fields = ['name', 'task', 'description', 'task_type', 'enabled', 'task_creator__employee__username']
    search_fields = ['name', 'task', 'description', 'task_type', 'enabled', 'task_creator__employee__username']
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


class WorkPeriodicTaskResultViewSet(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = TaskResult.objects.all()
    serializer_class = WorkPeriodicTaskResultSerializer
    filterset_fields = ['task_id', 'periodic_task_name', 'task_name', 'status', 'result',
                        'date_created', 'date_done', 'traceback']
    search_fields = ['task_id', 'periodic_task_name', 'task_name', 'status', 'result', 'date_created',
                     'date_done', 'traceback', 'worker', 'content_type']
    pagination_class = StandardResultsSetPagination


class ClockedScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
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


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
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


class CrontabScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
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


class SelectBoxClockedViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectBoxClockedSerializer
    queryset = ClockedSchedule.objects.all()
    pagination_class = StandardResultsSetPagination


class SelectBoxCrontabViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectBoxCrontabSerializer
    queryset = CrontabSchedule.objects.all()
    pagination_class = StandardResultsSetPagination


class SelectBoxIntervalViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectBoxIntervalSerializer
    queryset = IntervalSchedule.objects.all()
    pagination_class = StandardResultsSetPagination