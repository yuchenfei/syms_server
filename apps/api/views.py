from datetime import datetime

from django.contrib.auth import get_user_model, login, logout
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, permissions, exceptions, pagination, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.compat import authenticate
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.views import APIView, exception_handler

from exam.models import ExamSetting
from exam.serializers import ExamSettingSerializer
from experiment.models import Experiment, Item
from experiment.serializers import ExperimentSerializer, ItemSerializer
from info.models import User, Classes, Course, Student
from info.serializers import UserSerializer, ClassesSerializer, CourseSerializer, StudentSerializer
from thinking.models import Thinking
from thinking.serializers import ThinkingSerializer


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(context['view'], LoginView):
            # 登陆失败
            if isinstance(exc, exceptions.AuthenticationFailed):
                response.status_code = 200
                response.data['status'] = 'error'
                response.data['currentAuthority'] = 'guest'
                del response.data['detail']

    return response


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('userName', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed()

        credentials = {
            get_user_model().USERNAME_FIELD: username,
            'password': password
        }
        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed()
        if not user.is_active:
            raise exceptions.AuthenticationFailed()

        login(request, user)
        return JsonResponse({
            'status': 'ok',
            'currentAuthority': 'admin' if user.is_admin else 'user'
        })


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return JsonResponse({
            'status': 'ok'
        })


class CurrentUserView(APIView):
    def get(self, request):
        user = request.user
        if isinstance(user, User):
            name = user.last_name + user.first_name
            return JsonResponse({
                'userid': user.id,
                'name': name if name else user.username
            })


# 暂时解决csrf问题
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


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
        print(request.data)
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


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Experiment.objects.all()
        name = self.request.query_params.get('name', '')
        course = self.request.query_params.get('course', '')
        if course:
            queryset = queryset.filter(course=course)
        if name:
            queryset = queryset.filter(name=name)
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
        return super().create(request, *args, **kwargs)


class ThinkingViewSet(viewsets.ModelViewSet):
    queryset = Thinking.objects.all()
    serializer_class = ThinkingSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Thinking.objects.all()
        item = self.request.query_params.get('item', None)
        if item:
            queryset = queryset.filter(item=item)
        return queryset
