from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
# 实现定义的有一个uauth(app) models.py 表格Users
import json

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        if request.method == 'POST' or request.method=='PUT':
          if request.content_type=='application/json' and type(request.body) == bytes:
            request.bodyJson = json.loads(request.body)
        if request.path != '/login/' and request.path == '/register/' and request.method!='OPTIONS':
            # 从cookies中找ticket
            ticket = request.user.is_authenticated
            # 判断cookies中有没有ticket
            if not ticket:
                response = HttpResponse()
                response.status_code = 401
                return response


