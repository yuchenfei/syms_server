from django.apps import AppConfig

from .menu import create_menu


class WxConfig(AppConfig):
    name = 'wx'

    # TODO:部署时取消注释
    # def ready(self):
    #     create_menu()
