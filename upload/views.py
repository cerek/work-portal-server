from django.utils.crypto import get_random_string
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from upload.models import Upload
from upload.serializers import UploadSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class UploadViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ['file_name']
    search_fields = ['file_name']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        upload_file_name = serializer.validated_data.get('file_name', '')
        upload_file_url = serializer.validated_data.get('file_url', '')
        if not upload_file_name:
            random_string = get_random_string()
            split_list = upload_file_url.name.split('.')
            split_list.insert(-1, f'_{random_string}.')
            upload_file_name = ''.join(split_list)
        serializer.save(file_uploader=self.request.user.username,
                        file_name=upload_file_name)

    def destroy(self, request, *args, **kwargs):
        delete_obj = self.get_object()
        obj_serializer = self.get_serializer(self.get_object()).data
        try:
            delete_obj.delete()
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        # Return the deleted object to client.
        return Response(obj_serializer, status=status.HTTP_200_OK)
