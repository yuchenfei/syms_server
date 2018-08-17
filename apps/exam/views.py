from datetime import datetime

from rest_framework import viewsets, permissions

from api.views import CsrfExemptSessionAuthentication
from .models import ExamSetting, Question
from .serializers import ExamSettingSerializer, QuestionSerializer


class ExamSettingViewSet(viewsets.ModelViewSet):
    queryset = ExamSetting.objects.all()
    serializer_class = ExamSettingSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = ExamSetting.objects.filter(teacher=user)
        date = self.request.query_params.get('date', None)
        if date:
            date = datetime.strptime(date, '%Y-%m-%d')
            queryset = queryset.filter(datetime__date=date)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['teacher'] = request.user.id
        return super().create(request, *args, **kwargs)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Question.objects.all()
        item = self.request.query_params.get('item', None)
        if item:
            queryset = queryset.filter(item=item)
        return queryset
