from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    path('', views.WXAuthView.as_view()),
    path('login', views.Login.as_view(), name='login'),
    path('authorized', views.Authorized.as_view(), name='authorized'),
    path('binding', views.binding, name='binding'),
    path('home', views.home, name='home'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback_item/<int:experiment_id>/', views.feedback_item, name='feedback-item'),
    path('feedback_success/<int:experiment_id>/', views.feedback_success, name='feedback-success'),
    path('thinking', views.thinking, name='thinking'),
    path('thinking_item/<int:experiment_id>/', views.thinking_item, name='thinking-item'),
    path('grade', views.grade, name='grade'),
    path('grade_item/<int:grade_id>/', views.grade_item, name='grade-item'),

]
