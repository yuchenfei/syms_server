import functools
import hashlib

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView

from info.models import Student
from syms_server import settings
from .api.login import Login
from .utils import reverse_absolute_url, redirect_with_next_url

wx_login = Login(app_id=settings.APP_ID, app_secret=settings.APP_SECRET)


class WXAuthView(APIView):
    """用于认证服务器"""

    def get(self, request):
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = 'experiment'
        list = [token, timestamp, nonce]
        list.sort()
        hashcode = ''.join(list)
        hashcode = hashlib.sha1(hashcode.encode('utf8')).hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse()


class Login(View):
    """跳转至微信授权页面，获取code"""

    def get(self, request):
        next_url = request.GET.get('next')
        redirect_uri = reverse_absolute_url(request, 'authorized') + '?next={}'.format(next_url)
        url = wx_login.authorize(redirect_uri, "snsapi_base")
        return redirect(url)


class Authorized(View):
    """获取授权后微信回调页面"""

    def get(self, request):
        code = request.GET.get('code')
        next_url = request.GET.get('next')
        if not code:
            return Http404
        data = wx_login.access_token(code)
        openid = data.get('openid')
        if openid:
            response = redirect(next_url)
            response.set_cookie('openid', openid)
        else:
            response = Http404
        return response


def openid_required(func):
    """检查Cookie中是否有openid，没有则跳转至微信授权API"""

    @functools.wraps(func)
    def wrapper(request, *args, **kw):
        openid = request.COOKIES.get('openid')
        if openid:
            if not Student.objects.filter(openid=openid).exists():
                return redirect_with_next_url(request, 'binding', func.__name__)
            student = Student.objects.get(openid=openid)
            return func(request, student, *args, **kw)
        else:
            return redirect_with_next_url(request, 'login', func.__name__)

    return wrapper


def binding(request):
    if request.method == 'POST':
        xh = request.POST.get('xh')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        openid = request.COOKIES.get('openid')
        if Student.objects.filter(xh=xh).exists():
            student = Student.objects.get(xh=xh)
            if password == student.password:
                student.openid = openid
                student.save()
                return redirect(next_url)
        messages.add_message(request, messages.ERROR, "学号或密码错误！")
    else:
        next_url = request.GET.get('next')
    data = dict()
    data.setdefault('url', reverse('binding'))
    data.setdefault('next', next_url)
    return render(request, 'wx/binding.html', data)


@openid_required
def home(request, student=None):
    return HttpResponse(student.name)
