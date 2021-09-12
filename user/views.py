from typing import Dict
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from user.models import User, Group, Business, GroupEnum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from django.conf import settings
from file.models import Attachment
from utils.JsonParser import JsonParser
import re


class RegisterView(View):
    """注册"""

    def post(self, request):
        """进行注册处理"""
        # 接收数据
        response = HttpResponse()
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 进行数据校验
        if not all([password, email]):
            # 数据不完整
            response.status_code = 400
            response.content = '缺少用户名或密码'
            return response

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            response.status_code = 400
            response.content = '邮箱格式错误'
            return response

        # 校验用户名是否重复
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 用户名不存在，可用
            user = None

        if user:
            # 用户名存在
            response.status_code = 400
            response.content = '邮箱已存在'
            return response

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(email, password)
        # 激活字段，默认为没有激活
        user.is_active = 1
        user.save()
        # 发送激活邮件，包含激活连接： http：//127.0.0.1：8000/user/active/用户id
        # 激活连接中需要包含用户的身份信息，并且要把身份信息进行加密处理

        # 返回应答,跳转到首页
        return redirect('login/')


class LoginView(View):
    """登陆"""
    def post(self, request):
        """登陆校验"""
        # 接受数据
        email = request.POST.get('email')
        password = request.POST.get('password')
        response  = HttpResponse()
        # 校验数据
        if not all([email, password]):
            response.status_code=400
            response.content='缺少用户名或密码'
            return response

        # 业务处理： 登陆校验
        # 自动密码加密对比
        user = authenticate(email=email, password=password)
        if user is not None:
            # 用户名已激活
            login(request, user)
            # 跳转到首页
            return redirect('/')
        else:
            response = HttpResponse()
            response.status_code = 401
            response.content = '用户名或密码错误'
            return response




# user logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """退出登录"""
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect('login/')


# 用户信息
class UserInfo(View):
   
    def get(self,request):
        return JsonResponse(request.user.get_detail())

    # 更新个人信息
    def put(self,request):
        response = HttpResponse('修改成功')
        need_keys = ['username','sex','phone','age','picture']
        req_body = JsonParser(request.body)
        update_dict = req_body.getValues(need_keys)
        try:
            User.objects.filter(id=request.user.id).update(**update_dict)
        except :
            response.content = '修改失败'
            response.status_code=400
        return response

def updatePwd(request):
    if request.methods=='PUT':
        req_body = JsonParser(request.body)
        password = req_body.getValue('password')
        try:
            User.objects.filter(id=request.user.id).update(password=password)
        except :
            response = HttpResponse('修改失败')
            response.status_code=400
        return redirect('login/')