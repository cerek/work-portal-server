from rest_framework import viewsets, mixins
from systemlogs.models import Systemlogs
from systemlogs.serializers import SystemlogsSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class SystemlogsViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [ExtendViewPermission]
    serializer_class = SystemlogsSerializer
    queryset = Systemlogs.objects.all()
    filterset_fields = ['systemlog_operator', 'systemlog_operator_dept', 'systemlog_operate_module', 'systemlog_request_method',
                        'systemlog_request_ip', 'systemlog_request_agent', 'systemlog_request_time', 'systemlog_response_code']
    search_fields = ['systemlog_operator', 'systemlog_operator_dept', 'systemlog_operate_module', 'systemlog_request_method',
                     'systemlog_request_ip', 'systemlog_request_agent', 'systemlog_request_body', 'systemlog_request_time', 'systemlog_response_code']
    pagination_class = StandardResultsSetPagination
