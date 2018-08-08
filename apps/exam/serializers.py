from rest_framework import serializers

from .models import ExamSetting


class ExamSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSetting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['datetime'] = instance.datetime.strftime('%Y-%m-%d')  # %H:%M:%S
        course = instance.experiment.course
        representation['info'] = '{}({})'.format(course.name, course.classes.name)
        return representation
