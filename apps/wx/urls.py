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
]
