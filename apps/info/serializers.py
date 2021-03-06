from rest_framework import serializers

from .models import User, Classes, Course, Student


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


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['info'] = '{}【{}】'.format(instance.name, instance.classes.name)
        return representation


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
