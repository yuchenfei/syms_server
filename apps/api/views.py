from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from rest_framework import exceptions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler

from info.models import User


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
        if context['view'].__class__.handle_err_response:
            response = context['view'].__class__.handle_err_response(exc, context, response)
    return response


# 暂时解决csrf问题
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class LoginView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

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
                'currentUser': {
                    'userid': user.id,
                    'name': name if name else user.username,
                    'last_name': user.last_name,
                    'first_name': user.first_name,
                },
                'currentAuthority': 'admin' if user.is_admin else 'user'
            })
        response = Response()
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


class SettingView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        password_new = request.data.get('password_new')
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')
        json = {'status': 'ok'}
        if not user.check_password(password):
            json['status'] = 'error'
            return JsonResponse(json)
        user.last_name = last_name
        user.first_name = first_name
        if password_new:
            user.set_password(password_new)
        user.save()
        return JsonResponse(json)
