import requests
from idna import unicode
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView


class ExtView(APIView):
    url = ''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call_api(self, request, *args, **kwargs):
        headers = {}
        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }
        response = Response(method_map[method](self.url, headers=headers, data=json.dumps(request.data)).json())
        return response

    def get(self, request, *args, **kwargs):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return self.call_api(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return self.call_api(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return self.call_api(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return self.call_api(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return self.call_api(request, *args, **kwargs)
