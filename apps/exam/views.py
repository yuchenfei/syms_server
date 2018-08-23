import random
from datetime import datetime

from rest_framework import viewsets, permissions

from api.views import CsrfExemptSessionAuthentication
from experiment.models import Experiment
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
        experiment = Experiment.objects.get(id=request.data['experiment'])
        question_list = Question.objects.filter(item=experiment.item)
        if question_list.exists():
            if question_list.count() > 10:
                question_list = random.sample(list(question_list), 10)
            else:
                question_list = question_list.all()
            request.data['questions'] = ','.join([str(exam.id) for exam in question_list])
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
