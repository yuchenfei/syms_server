import functools
import hashlib
import random

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView

from experiment.models import Experiment, Feedback
from info.models import Student, Course
from syms_server import settings
from thinking.models import Thinking
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


def student_required(func):
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
    """学生绑定登陆视图"""
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


@student_required
def home(request, student=None):
    return HttpResponse(student.name)


@student_required
def feedback(request, student=None):
    course_list = Course.objects.filter(classes=student.classes).all()
    experiment_data = dict()
    for course in course_list:
        experiment_list = Experiment.objects.filter(course=course).all()
        experiment_data.setdefault(course, experiment_list)
    feedback_list = Feedback.objects.filter(student=student).all()
    data = dict()
    data.setdefault('experiment_data', experiment_data)
    data.setdefault('feedback_list', [i.experiment.id for i in feedback_list])
    return render(request, 'wx/feedback.html', data)


def get_random_thinking(item):
    thinking_list = Thinking.objects.filter(item=item)
    if thinking_list.exists():
        return random.sample(list(thinking_list), 1)[0]
    else:
        return None


@student_required
def feedback_item(request, student=None, experiment_id=None):
    experiment = Experiment.objects.get(id=experiment_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        images = request.FILES
        if not content:
            return JsonResponse({'status': 'error', 'errMsg': '反馈内容为空'})
        _feedback = Feedback(
            experiment=experiment,
            student=student,
            content=content,
        )
        _thinking = get_random_thinking(experiment.item)
        if _thinking:
            _feedback.thinking_id = _thinking.id
        for index, key in enumerate(images):
            setattr(_feedback, 'image' + str(index + 1), images[key])
        try:
            _feedback.save()
        except IntegrityError:
            return JsonResponse({'status': 'error', 'errMsg': '已反馈'})
        url = request.build_absolute_uri(reverse('feedback-success', args=(experiment_id,)))
        return JsonResponse({'status': 'ok', 'url': url})
    else:
        if Feedback.objects.filter(experiment=experiment, student=student).exists():
            _feedback = Feedback.objects.get(experiment=experiment, student=student)
            images = []
            for i in range(1, 6):
                image = getattr(_feedback, 'image{}'.format(i))
                if image:
                    url = request.build_absolute_uri(image.url)
                    images.append(url)
            return render(request, 'wx/feedback_item.html', {'feedback': _feedback, 'images': images})
        return render(request, 'wx/feedback_upload.html', {'id': experiment_id})


@student_required
def feedback_success(request, student=None, experiment_id=None):
    experiment = Experiment.objects.get(id=experiment_id)
    return render(request, 'wx/feedback_success.html', {'experiment': experiment})


@student_required
def thinking(request, student=None):
    feedback_list = Feedback.objects.filter(student=student).all()
    experiment_list = [i.experiment for i in feedback_list]
    course_list = set(Course.objects.filter(experiment__in=experiment_list).all())
    data = dict()
    data.setdefault('course_list', course_list)
    data.setdefault('experiment_list', experiment_list)
    return render(request, 'wx/thinking.html', data)


@student_required
def thinking_item(request, student=None, experiment_id=None):
    experiment = Experiment.objects.get(id=experiment_id)
    _feedback = Feedback.objects.get(experiment=experiment, student=student)
    _thinking = Thinking.objects.filter(id=_feedback.thinking_id)
    if not _thinking.exists():  # 不存在思考题时尝试选择，题库为空则在模板中显示
        _thinking = get_random_thinking(experiment.item)
        if _thinking:
            _feedback.thinking_id = _thinking.id
            _feedback.save()
    else:
        _thinking = _thinking.first()
    return render(request, 'wx/thinking_item.html', {'thinking': _thinking, 'experiment': experiment})
