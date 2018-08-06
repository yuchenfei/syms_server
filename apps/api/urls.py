from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('classes', views.ClassesViewSet)
router.register('course', views.CourseViewSet)

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('currentUser', views.CurrentUserView.as_view()),
    path('', include(router.urls)),
]
