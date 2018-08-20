from django.apps import AppConfig

from .menu import create_menu


class WxConfig(AppConfig):
    name = 'wx'
