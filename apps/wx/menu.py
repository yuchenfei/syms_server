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
                        "name": "在线答题",
                        "url": "http://syms-server.flyingspace.cn/wx/exam_select"
                    },
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
                        "url": "http://syms-server.flyingspace.cn/wx/grade"
                    },
                    {
                        "type": "view",
                        "name": "个人设置",
                        "url": "http://syms-server.flyingspace.cn/wx/setting"
                    }
                ]
            }
        ]
    }
    """
    official_account = MyOfficialAccounts()
    print('创建微信自定义菜单:')
    print(official_account.create_menu(menu))
