# django.contrib.auth.backends获取auth模块的验证和用户的信息
from django.contrib.auth.backends import BaseBackend
from UserInfo.models import User
from django.db.models import Q


class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=email) & Q(password=password))
            if user is not None:
                return user

        except Exception as e:
            print(email, password)
            return None
            
    def get_user(self, user_id):
        user = User.objects.get(Q(id=user_id))
        return user
