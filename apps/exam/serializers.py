from rest_framework import serializers

from .models import ExamSetting


class ExamSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSetting
        fields = '__all__'
