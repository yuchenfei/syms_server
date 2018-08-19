from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse

from syms_server import settings
from .api.official_accounts import OfficialAccounts

Token_key = 'access_token'


class MyOfficialAccounts(OfficialAccounts):
    def __init__(self):
        super().__init__(app_id=settings.APP_ID, app_secret=settings.APP_SECRET)

    def get_access_token(self):
        return cache.get(Token_key)

    def save_access_token(self, access_token, expires_in):
        cache.set(Token_key, access_token, expires_in)


def reverse_absolute_url(request, view_name):
    return request.build_absolute_uri(reverse(view_name))


def redirect_with_next_url(request, view_name, next_view_name):
    next_url = reverse_absolute_url(request, next_view_name)
    url = reverse_absolute_url(request, view_name) + '?next={}'.format(next_url)
    return redirect(url)