import os

from wx.api.official_accounts import OfficialAccounts


def create_menu():
    menu = """
    {
        "button":
        [
            {
                "type": "view",
                "name": "文件",
                "url": "http://www.ustslab.com/wx/file"
            },
            {
                "name": "实验",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "在线答题",
                        "url": "http://www.ustslab.com/wx/exam_select"
                    },
                    {
                        "type": "view",
                        "name": "反馈",
                        "url": "http://www.ustslab.com/wx/feedback"
                    },
                    {
                        "type": "view",
                        "name": "思考题",
                        "url": "http://www.ustslab.com/wx/thinking"
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
                        "url": "http://www.ustslab.com/wx/grade"
                    },
                    {
                        "type": "view",
                        "name": "个人设置",
                        "url": "http://www.ustslab.com/wx/setting"
                    }
                ]
            }
        ]
    }
    """
    official_account = OfficialAccounts(app_id=os.environ.get('APP_ID'), app_secret=os.environ.get('APP_SECRET'))
    print('创建微信自定义菜单:')
    print(official_account.create_menu(menu))


if __name__ == '__main__':
    create_menu()
