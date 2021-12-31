from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
# 实现定义的有一个uauth(app) models.py 表格Users
import json

noNeedPath = ['/api/file/upload/','/api/auth/login/','/api/auth/register/']
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        if request.method == 'POST' or request.method=='PUT':
          if request.content_type=='application/json' and type(request.body) == bytes:
            request.bodyJson = json.loads(request.body)


