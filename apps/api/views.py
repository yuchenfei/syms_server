from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from rest_framework import viewsets, permissions, exceptions, pagination, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.compat import authenticate
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler

from info.models import User
from info.serializers import UserSerializer


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
