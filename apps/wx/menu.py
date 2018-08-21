from wx.utils import MyOfficialAccounts


def create_menu():
    # TODO：部署时修改域名
    menu = """
    {
        "button":
        [
            {
                "name": "实验",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "反馈",
                        "url": "http://syms-server.flyingspace.cn/wx/feedback"
                    },
                    {
                        "type": "view",
                        "name": "思考题",
                        "url": "http://syms-server.flyingspace.cn/wx/thinking"
                    }
                ]
            },
            {
                "name": "我的",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "成绩",
                        "url": "http://syms-server.flyingspace.cn/wx/home"
                    },
                    {
                        "type": "view",
                        "name": "修改密码",
                        "url": "http://syms-server.flyingspace.cn/wx/home"
                    }
                ]
            }
        ]
    }
    """
    official_account = MyOfficialAccounts()
    official_account.create_menu(menu)
