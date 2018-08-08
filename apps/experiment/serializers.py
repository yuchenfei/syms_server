from rest_framework import serializers

from .models import Experiment, Item


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
        representation['info'] = '{}({})'.format(instance.course.name, instance.course.classes.name)
        return representation
