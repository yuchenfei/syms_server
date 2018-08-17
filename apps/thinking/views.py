from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser

from api.views import CsrfExemptSessionAuthentication
from .models import Thinking
from .serializers import ThinkingSerializer


class ThinkingViewSet(viewsets.ModelViewSet):
    queryset = Thinking.objects.all()
    serializer_class = ThinkingSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Thinking.objects.all()
        item = self.request.query_params.get('item', None)
        if item:
            queryset = queryset.filter(item=item)
        return queryset
