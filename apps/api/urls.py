from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('classes', views.ClassesViewSet)
router.register('course', views.CourseViewSet)
router.register('student', views.StudentViewSet)
router.register('exam', views.ExamSettingViewSet)
router.register('item', views.ItemViewSet)
router.register('experiment', views.ExperimentViewSet)
router.register('thinking', views.ThinkingViewSet)

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('currentUser', views.CurrentUserView.as_view()),
    path('', include(router.urls)),
]
