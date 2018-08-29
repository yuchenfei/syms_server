from rest_framework import serializers

from .models import Experiment, Item, Feedback, Grade


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.item.name
        representation['info'] = '{}【{}】'.format(instance.course.name, instance.course.classes.name)
        return representation


class FeedbackSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for i in range(1, 6):
            image = getattr(obj, 'image{}'.format(i))
            if image:
                url = request.build_absolute_uri(image.url)
                images.append({
                    'src': url,
                    'orientation': 'landscape',
                })
        return images

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['datetime'] = instance.datetime.strftime('%Y-%m-%d %H:%M')  # %H:%M:%S
        representation['experimentName'] = instance.experiment.item.name
        representation['courseName'] = instance.experiment.course.name
        representation['studentName'] = instance.student.name
        representation['studentXH'] = instance.student.xh
        return representation


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['xh'] = instance.student.xh
        representation['studentName'] = instance.student.name
        return representation
