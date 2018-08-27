from rest_framework import viewsets, permissions
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
