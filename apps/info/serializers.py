from django.conf import settings
from rest_framework import serializers

from info.models import User, Classes


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'name', 'is_admin')

    def get_name(self, obj):
        return '{}{}'.format(obj.last_name, obj.first_name)


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'
