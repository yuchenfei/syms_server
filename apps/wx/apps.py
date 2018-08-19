from django.apps import AppConfig
from django.core.cache import cache

from syms_server import settings
from .utils import MyOfficialAccounts

Token_key = 'access_token'


class WxConfig(AppConfig):
    name = 'wx'

    def ready(self):  # 启动时创建微信公众号自定义目录
        menu = """
        {
            "button":
            [
                {
                    "name": "我的",
                    "sub_button":
                    [
                        {
                            "type": "view",
                            "name": "主页",
                            "url": "http://syms-server.flyingspace.cn/wx/home"
                        },
                    ]
                }
            ]
        }
        """
        official_account = MyOfficialAccounts()
        official_account.create_menu(menu)
