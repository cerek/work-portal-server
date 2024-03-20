from rest_framework import status
from rest_framework.response import Response
from systemlogs.models import Systemlogs
import json
import time


REQUEST_METHOD_CHOICES = {
    'GET': 0,
    'POST': 1,
    'PUT': 2,
    'PATCH': 3,
    'DELETE': 4,
}


class SystemlogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request_body = ''
        if request.method not in ['GET', 'DELETE']:
            request_body = json.loads(request.body)
            if 'password' in request_body:
                request_body['password'] = '**********'
        else:
            request_body = '-'

        new_log_data = {
            "systemlog_request_body": request_body,
        }

        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        time_duration = round(end_time - start_time, 4)
        new_log_data.update({
            "systemlog_operator": request.user.employee,
            "systemlog_operate_module": request.get_full_path(),
            "systemlog_request_method": REQUEST_METHOD_CHOICES.get(request.method),
            "systemlog_request_ip": request.headers.get('User-Ip-Address', '0.0.0.0'),
            "systemlog_request_agent": request.headers.get('User-Agent', '-'),
            "systemlog_response_code": response.status_code,
            "systemlog_response_duration": time_duration,
        })

        response_data = '-'
        if request.method != 'GET':
            response_data = json.dumps(response.data)
        new_log_data.update({
            "systemlog_response_context": response_data
        })

        try:
            Systemlogs.objects.create(**new_log_data)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        return response
