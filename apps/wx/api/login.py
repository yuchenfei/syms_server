import requests


class Login(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def authorize(self, redirect_uri, scope="snsapi_base", state=None):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize"
        assert scope in ["snsapi_base", "snsapi_userinfo"]
        params = dict()
        params.setdefault("appid", self.app_id)
        params.setdefault("redirect_uri", redirect_uri)
        params.setdefault("response_type", "code")
        params.setdefault("scope", scope)
        if state:
            params.setdefault("state", state)
        data = [(k, params[k]) for k in sorted(params.keys()) if params[k]]
        return "{0}?{1}#wechat_redirect".format(url, "&".join("=".join(kv) for kv in data if kv[1]))

    def access_token(self, code):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        params = dict()
        params.setdefault("appid", self.app_id)
        params.setdefault("secret", self.app_secret)
        params.setdefault("code", code)
        params.setdefault("grant_type", "authorization_code")
        response = requests.get(url, params).json()
        return response
