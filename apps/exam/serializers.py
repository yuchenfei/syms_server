from datetime import datetime, timedelta

from rest_framework import serializers

from .models import ExamSetting, Question


class ExamSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSetting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['datetime'] = instance.datetime.strftime('%Y-%m-%d')  # %H:%M:%S
        course = instance.experiment.course
        representation['info'] = '{}({})'.format(course.name, course.classes.name)
        if (datetime.now() - instance.datetime) > timedelta(minutes=(instance.duration + 1)):
            representation['report'] = 'ok'
        return representation


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
