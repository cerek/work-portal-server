from rest_framework import viewsets, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ticket.models import Ticket, TicketType
from ticket.serializers import TicketSerializer, TicketTypeSerializer, MyTicketSerializer, SelectBoxTicketTypeSerializer, MyDeptTicketSerializer
from ticket.permissions import ViewMyTicketPermission, ViewMyDeptTicketPermission
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.conf import settings
import pytz
import random


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filterset_fields = ['ticket_title', 'ticket_creator', 'ticket_assign_department', 'ticket_assigner', 'ticket_description', 'ticket_status']
    search_fields = ['ticket_title', 'ticket_creator__employee__username', 'ticket_assign_department__department__name', 'ticket_description', 'ticket_assigner__employee__username']
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


class TicketTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    filterset_fields = ['ticket_type_name']
    search_fields = ['ticket_type_name']
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


class SelectBoxTicketTypeViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TicketType.objects.all()
    serializer_class = SelectBoxTicketTypeSerializer
    filterset_fields = ['ticket_type_name']
    search_fields = ['ticket_type_name']
    pagination_class = StandardResultsSetPagination


class TicketKanbanViewSet(ListAPIView):
    permission_classes = []
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filterset_fields = ['ticket_title', 'ticket_creator_name', 'ticket_creator_dept', 'ticket_assigner', 'ticket_description', 'ticket_status']
    search_fields = ['ticket_title', 'ticket_creator_name', 'ticket_creator_dept', 'ticket_description']
    pagination_class = StandardResultsSetPagination


# class TicketReportViewSet(APIView):
#     permission_classes = [ViewReportPermission]
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer

#     def get(self, request):
#         query_params_dict = request.query_params
#         start_day_str = query_params_dict.get('start_day', '')
#         end_day_str = query_params_dict.get('end_day', '')
#         tz = pytz.timezone(settings.TIME_ZONE)
#         if start_day_str:
#             start_day = tz.localize(datetime.strptime(start_day_str, '%Y-%m-%d'))
#         else:
#             start_day = tz.localize(datetime.now() - timedelta(days=30))

#         if end_day_str:
#             end_day = tz.localize(datetime.strptime(end_day_str, '%Y-%m-%d'))
#         else:
#             end_day = tz.localize(datetime.now())

#         qs_res = Ticket.objects.all()
#         # Time range filter
#         if 'time_style' in query_params_dict:
#             if query_params_dict.get('time_style') == 'created_time':
#                 qs_res = qs_res.filter(created_time__range=[start_day, end_day])
#             elif query_params_dict.get('time_style') == 'final_time':
#                 qs_res = qs_res.filter(ticket_final_time__range=[start_day, end_day])

#         # Condiction filter
#         if 'ticket_creator_name' in query_params_dict:
#             creator_list = query_params_dict.get('ticket_creator_name')
#             creator_list = creator_list.split(',')
#             qs_res = qs_res.filter(ticket_creator_name__in=creator_list)
#         if 'ticket_creator_dept' in query_params_dict:
#             creator_dept_list = query_params_dict.get('ticket_creator_dept')
#             creator_dept_list = creator_dept_list.split(',')
#             qs_res = qs_res.filter(ticket_creator_dept__in=creator_dept_list)
#         if 'ticket_status' in query_params_dict:
#             ticket_status_list = query_params_dict.get('ticket_status')
#             ticket_status_list = ticket_status_list.split(',')
#             qs_res = qs_res.filter(ticket_status__in=ticket_status_list)
#         if 'ticket_assigner_name' in query_params_dict:
#             assinger_list = query_params_dict.get('ticket_assigner_name')
#             assinger_list = assinger_list.split(',')
#             qs_res = qs_res.filter(ticket_assigner_name__in=assinger_list)

#         # Dimension Generate result
#         # LineChart: 30day-total, 
#         # PieChart: department-share, creator-share, assigner-share, status-share,
#         # VerBarChart: assigner-count
#         # HorBarChart: top20-rank
#         res_data = {}
#         if 'dimension_type' in query_params_dict:
#             dimension_type = query_params_dict.get('dimension_type')
#             if dimension_type == '30day-total':
#                 days_label = [(start_day + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_day - start_day).days + 1)]
#                 data_list = []
#                 qs_res = qs_res.values('created_time__date').annotate(Total=Count(id)).order_by('created_time__date')
#                 for obj in qs_res:
#                     data_list.append(obj['Total'])
#                 res_data['labels'] = days_label
#                 res_data['datasets'] = [{'label': dimension_type, 'data': data_list, 'borderColor': 'rgb(255, 99, 132)', 'backgroundColor': 'rgba(255, 99, 132, 0.5)'}]
#                 return Response(res_data, status=status.HTTP_200_OK)
#             elif dimension_type in ['department-share', 'creator-share', 'assigner-share', 'status-share']:
#                 convert_dict = {'department-share': 'ticket_creator_dept', 'creator-share':'ticket_creator_name', 'assigner-share': 'ticket_assigner_name', 'status-share': 'ticket_status'}
#                 dimension_label = [ x[0] for x in set(qs_res.values_list(convert_dict[dimension_type]))]
#                 data_list = []
#                 qs_res = qs_res.values(convert_dict[dimension_type]).annotate(Total=Count(id)).order_by(convert_dict[dimension_type])
#                 for obj in qs_res:
#                     data_list.append(obj['Total'])
#                 res_data['labels'] = dimension_label
#                 res_data['datasets'] = [{'data': data_list, 'backgroundColor': [f'rgba{random.randint(1,255), random.randint(1,255), random.randint(1,255), random.uniform(0, 1)}' for x in range(len(dimension_label))]}]
#                 return Response(res_data, status=status.HTTP_200_OK)
#             elif dimension_type == 'top20-rank':
#                 dimension_label = []
#             elif dimension_type == 'assigner-count':
#                 dimension_label = [(start_day + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_day - start_day).days + 1)]
#                 data_dict = {}
#                 datasets_list = []
#                 qs_res = qs_res.values('created_time__date','ticket_assigner_name').annotate(Total=Count(id)).order_by('created_time__date', 'ticket_assigner_name')
#                 print(qs_res)
#                 for obj in qs_res:
#                     if obj['ticket_assigner_name'] not in data_dict:
#                         data_dict[obj['ticket_assigner_name']] = []
#                         data_dict[obj['ticket_assigner_name']].append(obj['Total'])
#                     else:
#                         data_dict[obj['ticket_assigner_name']].append(obj['Total'])
#                 for k,v in data_dict.items():
#                     datasets_list.append({'label': f'{k}', 'data':v, 'backgroundColor':f'rgba{random.randint(1,255), random.randint(1,255), random.randint(1,255), random.uniform(0, 1)}'})
                
#                 res_data['labels'] = dimension_label
#                 res_data['datasets'] = datasets_list
#                 return Response(res_data, status=status.HTTP_200_OK)


class MyTicketViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [ViewMyTicketPermission]
    serializer_class = MyTicketSerializer
    filterset_fields = ['ticket_title', 'ticket_assign_department', 'ticket_assigner', 'ticket_description', 'ticket_status']
    search_fields = ['ticket_title', 'ticket_assign_department__department__name', 'ticket_description', 'ticket_status', 'ticket_assigner__employee__username']
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user = self.request.user
        qs = Ticket.objects.filter(ticket_creator=user.employee)
        return qs


class MyDeptTicketViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [ViewMyDeptTicketPermission]
    serializer_class = MyDeptTicketSerializer
    filterset_fields = ['ticket_title', 'ticket_assign_department', 'ticket_assigner', 'ticket_description', 'ticket_status', 'created_time']
    search_fields = ['ticket_title', 'ticket_assign_department__department__name', 'ticket_description', 'ticket_status', 'ticket_assigner__employee__username']
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user = self.request.user
        my_dept = user.employee.employee_department
        qs = Ticket.objects.filter(ticket_assign_department=my_dept)
        return qs