from django.shortcuts import redirect
from django.urls import reverse


def reverse_absolute_url(request, view_name):
    return request.build_absolute_uri(reverse(view_name))


def redirect_with_next_url(request, view_name, next_view_name):
    next_url = reverse_absolute_url(request, next_view_name)
    url = reverse_absolute_url(request, view_name) + '?next={}'.format(next_url)
    return redirect(url)
