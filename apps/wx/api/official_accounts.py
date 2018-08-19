import requests


class OfficialAccounts(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def get_access_token(self):
        return None

    def save_access_token(self, access_token, expires_in):
        pass

    @property
    def access_token(self):
        access_token = self.get_access_token()
        if access_token:
            return access_token
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = dict()
        params.setdefault('grant_type', 'client_credential')
        params.setdefault('appid', self.app_id)
        params.setdefault('secret', self.app_secret)
        response = requests.get(url, params).json()
        if 'errcode' in response:
            msg = '{}: {}'.format(response['errcode'], response['errmsg'])
            raise Exception(msg)
        access_token = response['access_token']
        expires_in = response['expires_in']
        self.save_access_token(access_token, expires_in)
        return access_token

    def create_menu(self, menu):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(self.access_token)
        if isinstance(menu, str):
            menu = menu.encode('utf-8')
        response = requests.post(url, data=menu)
        return response.text
