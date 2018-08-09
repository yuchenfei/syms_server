from rest_framework import serializers

from thinking.models import Thinking


class ThinkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thinking
        fields = '__all__'
