import functools
import hashlib
import json
import os
import random
from datetime import datetime, timedelta

from django.core.cache import cache
from django.db import IntegrityError
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView

from exam.models import ExamSetting, Question, ExamRecord
from experiment.models import Experiment, Feedback, Grade
from file.models import File
from info.models import Student, Course
from syms_server import settings
from thinking.models import Thinking
from .api.login import Login
from .utils import reverse_absolute_url, redirect_with_next_url

wx_login = Login(app_id=os.environ.get('APP_ID'), app_secret=os.environ.get('APP_SECRET'))


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
    data = dict()
    if request.method == 'POST':
        xh = request.POST.get('xh')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        openid = request.COOKIES.get('openid')
        if Student.objects.filter(xh=xh).exists():
            student = Student.objects.get(xh=xh)
            if password == student.password:
                if student.openid:
                    data.setdefault('errMsg', '账号已与其他微信绑定')
                else:
                    student.openid = openid
                    student.save()
                    return redirect(next_url)
            else:
                data.setdefault('errMsg', '学号或密码错误')
        else:
            data.setdefault('errMsg', '学号或密码错误')
    else:
        next_url = request.GET.get('next')
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
    image_url = ''
    if not _thinking.exists():  # 不存在思考题时尝试选择，题库为空则在模板中显示
        _thinking = get_random_thinking(experiment.item)
        if _thinking:
            _feedback.thinking_id = _thinking.id
            _feedback.save()
    else:
        _thinking = _thinking.first()
        if _thinking.picture:
            image_url = request.build_absolute_uri(_thinking.picture.url)
    data = dict()
    data.setdefault('experiment', experiment)
    data.setdefault('thinking', _thinking)
    data.setdefault('image', image_url)
    return render(request, 'wx/thinking_item.html', data)


@student_required
def grade(request, student=None):
    grade_list = Grade.objects.filter(student=student).all()
    experiment_list = [i.experiment for i in grade_list]
    course_list = set(Course.objects.filter(experiment__in=experiment_list).all())
    data = dict()
    data.setdefault('course_list', course_list)
    data.setdefault('grade_list', grade_list)
    data.setdefault('item_name', json.dumps([grade.experiment.item.name for grade in grade_list]))
    data.setdefault('data', json.dumps([grade.grade for grade in grade_list]))
    return render(request, 'wx/grade.html', data)


@student_required
def grade_item(request, student=None, grade_id=None):
    _grade = Grade.objects.get(id=grade_id)
    data = []
    queryset = Grade.objects.filter(experiment=_grade.experiment)
    data.append(queryset.filter(grade__lt=60).count())
    data.append(queryset.filter(grade__range=(60, 69)).count())
    data.append(queryset.filter(grade__range=(70, 79)).count())
    data.append(queryset.filter(grade__range=(80, 89)).count())
    data.append(queryset.filter(grade__range=(90, 100)).count())
    return render(request, 'wx/grade_item.html', {'grade': _grade, 'data': json.dumps(data)})


@student_required
def setting(request, student=None):
    if request.method == 'POST':
        name = request.POST.get('name')
        password_new = request.POST.get('password_new')
        password = request.POST.get('password')
        if password != student.password:
            return JsonResponse({'status': 'err', 'errMsg': '密码错误'})
        student.name = name
        student.password = password_new
        student.save()
        return JsonResponse({'status': 'ok'})
    return render(request, 'wx/setting.html', {'student': student})


@student_required
def exam_select(request, student=None):
    exam_query = ExamSetting.objects.filter(experiment__course__classes=student.classes).all()
    exam_list = list()
    for _exam in exam_query:
        # 过滤在有效时间内的在线答题设置
        if _exam.datetime + timedelta(minutes=_exam.duration) > datetime.now():
            exam_list.append(_exam)
    return render(request, 'wx/exam_select.html', {'exam_list': exam_list})


@student_required
def exam(request, student=None, exam_id=None):
    _exam = ExamSetting.objects.get(id=exam_id)
    if request.method == 'POST':
        options = json.loads(request.POST.get('options'))
        answer_key = 'exam_{}'.format(exam_id)
        answer = cache.get(answer_key)
        if not answer:
            questions = [Question.objects.get(id=i) for i in _exam.questions.split(',')]
            answer = dict()
            for question in questions:
                answer.setdefault(question.id, question.answer)
            cache.set(answer_key, answer, (_exam.duration + 5) * 60)  # 多存五分钟
        count = 0
        for option in options:
            if answer.get(option.get('id')) == option.get('option'):
                count = count + 1
        result = int(count * 100 / len(answer))
        record = ExamRecord(setting=_exam, student=student, result=result)
        record.save()
        return JsonResponse({'status': 'ok', 'result': result, 'count': count})
    # GET
    if ExamRecord.objects.filter(setting=_exam, student=student).exists():
        return render(request, 'wx/error.html', {'errMsg': '已完成答题'})
    questions_key = 'questions_{}'.format(exam_id)
    questions = cache.get(questions_key)
    if not questions:
        questions = [Question.objects.get(id=i) for i in _exam.questions.split(',')]
        cache.set(questions_key, questions, (_exam.duration + 5) * 60)
    question_list = [{
        'id': i.id,
        'title': i.title,
        'a': i.a,
        'b': i.b,
        'c': i.c,
        'd': i.d
    } for i in questions]
    random.shuffle(question_list)
    time_remain = int(_exam.duration) * 60 - (datetime.now() - _exam.datetime).seconds
    if time_remain < 0:
        time_remain = -1
    elif time_remain < 60:
        time_remain = 60
    print(time_remain)
    data = dict()
    data.setdefault('exam', _exam)
    data.setdefault('data', json.dumps(question_list))
    data.setdefault('time_remain', time_remain)
    return render(request, 'wx/exam.html', data)


def file(request):
    file_list = File.objects.all()
    return render(request, 'wx/file.html', {'file_list': file_list})
