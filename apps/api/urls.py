from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from info import views as info_views
from exam import views as exam_views
from thinking import views as thinking_views
from experiment import views as experiment_views

router = DefaultRouter()
router.register('users', info_views.UserViewSet)
router.register('classes', info_views.ClassesViewSet)
router.register('course', info_views.CourseViewSet)
router.register('student', info_views.StudentViewSet)
router.register('exam', exam_views.ExamSettingViewSet)
router.register('question', exam_views.QuestionViewSet)
router.register('thinking', thinking_views.ThinkingViewSet)
router.register('item', experiment_views.ItemViewSet)
router.register('experiment', experiment_views.ExperimentViewSet)
router.register('feedback', experiment_views.FeedbackViewSet)
router.register('grade', experiment_views.GradeViewSet)

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('currentUser', views.CurrentUserView.as_view()),
    path('setting', views.SettingView.as_view()),
    path('grade/import', experiment_views.GradeImportView.as_view()),
    path('exam/report/<int:exam_id>/', exam_views.Report.as_view(), name='exam-report'),
    path('', include(router.urls)),
]
