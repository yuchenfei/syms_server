from rest_framework import viewsets, permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from api.views import CsrfExemptSessionAuthentication
from .models import User, Classes, Course, Student
from .serializers import UserSerializer, ClassesSerializer, CourseSerializer, StudentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', '')
        is_admin = self.request.query_params.get('is_admin', None)
        if is_admin is not None:  # str to bool
            is_admin = True if 'true' == is_admin else False
            queryset = queryset.filter(is_admin=is_admin)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def create(self, request, *args, **kwargs):
        # 保存时生成用户名
        response = super().create(request, *args, **kwargs)
        if status.HTTP_201_CREATED == response.status_code:
            user = User.objects.get(username=request.data['username'])
            user.set_password('123456')
            user.save()
        return response

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Course.objects.all()
        name = self.request.query_params.get('name', '')
        _status = self.request.query_params.get('status', None)
        classes = self.request.query_params.get('classes', '')
        if classes:
            queryset = queryset.filter(classes=classes)
        if _status is not None:
            _status = True if 'true' == _status else False
            queryset = queryset.filter(status=_status)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Student.objects.all()
        name = self.request.query_params.get('name', '')
        classes = self.request.query_params.get('classes', '')
        if classes:
            queryset = queryset.filter(classes=classes)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
