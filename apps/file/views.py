from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from api.views import CsrfExemptSessionAuthentication
from .serializers import FileSerializer
from .models import File


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = File.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @staticmethod
    def handle_err_response(exc, context, response):
        if isinstance(exc, ValidationError):
            if exc.get_codes().get('name')[0] == 'unique':
                response.status_code = 200
                response.data['status'] = 'error'
                response.data['errMsg'] = '文件名已存在'
        return response
