from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from UserInfo.models import Promotion, User, Group, Shop
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from apps.File.models import Attachment
import json
import re

from decorator.auth import loginCheck

# Create your views here.

# 类视图的使用
# /user/register


class RegisterView(View):
    """注册"""

    def post(self, request):
        """进行注册处理"""
        # 接收数据
        response = HttpResponse()
        password = request.bodyJson.get('password')
        email = request.bodyJson.get('email')
        code = request.bodyJson.get('code')

        print(password)
        # 普通用户验证
        if code == 100:
            if not all([password, email, code]):
                # 数据不完整
                response.status_code = 400
                response.content = '缺少用户名或密码'
                return response
        # 商家用户验证
        elif code == 300:
            shop_name = request.bodyJson.get('shop_name')
            shop_desc = request.bodyJson.get('shop_desc')
            shop_thumb = request.bodyJson.get('shop_thumb')
            if not all([password, email, code, shop_name, shop_desc, shop_thumb]):
                # 数据不完整
                response.status_code = 400
                response.content = '缺少信息'
                return response
        else:
            response.status_code = 400
            response.content = '用户类型错误'
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
        user = User.objects.create_user(email=email, password=password)
        # 激活字段，默认为没有激活
        user.is_active = 1
        try:
            group = Group.objects.get(code=code)
            image = Attachment.objects.get(file_name='default')
        except Group.DoesNotExist:
            group_name = "客户" if code == 100 else 300
            group = Group.objects.create(code=code, name=group_name)
        except Attachment.DoesNotExist:
            image = Attachment.objects.create(
                file_name="default", file_path='default.jpg')
        user.group = group
        user.thumb = image
        user.save()

        if code == 300:
            try:
                file = Attachment.objects.get(id=shop_thumb['id'])
                Shop.objects.create(
                    name=shop_name, desc=shop_desc, thumb=file, user=user)
            except Attachment.DoesNotExist:
                response.status_code = 400
                response.content = '图片id错误'
                return response
            except Exception as e:
                print(e)
                response.status_code = 500
                response.content = '创建商铺失败'
                return response

        response.status_code = 200
        response.content = 'ok'
        return response


class LoginView(View):
    """登陆"""

    def post(self, request):
        """登陆校验"""
        # 接受数据
        email = request.bodyJson.get('email')
        password = request.bodyJson.get('password')
        response = HttpResponse()
        response.status_code = 200
        # 校验数据
        if not all([email, password]):
            response.status_code = 400
            response.content = "缺少用户名或密码"
            return response

        # 自动密码加密对比
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 用户名已激活
            login(request, user)
            # 跳转到首页
            return response
        else:
            response.status_code = 400
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
        return HttpResponse('登出成功！')

# /user
    """用户中心-信息页"""


class UserView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        if user.group.code == 300:
            shop = user.shop_set.all()[0]
            return HttpResponse(json.dumps({
                "email": user.email,
                "id": user.id,
                "shop_promotion": list(shop.promotion_set.all().values()),
                'shop_name': shop.name,
                "shop_thumb": shop.thumb_id,
                "shop_desc": shop.desc,
                "shop_autoAccept": shop.autoAccept
            }))
        elif user.group.code==100:
            return HttpResponse(json.dumps({
                "email": user.email,
                "vip_level": 0,
                "id": user.id,
                "abstract_money": user.abstract_money,
            }))

    @method_decorator(loginCheck)
    def put(self, request):
        type = request.bodyJson.get('type')
        user = request.user
        if type == 'pwd':
            password = request.bodyJson.get('password')
            oldPassword = request.bodyJson.get('oldPassword')
            if not all([password, oldPassword]):
                return HttpResponseBadRequest('参数错误')
            elif user.password != oldPassword:
                return HttpResponseBadRequest('参数错误')
            else:
                user.password = password
                user.save()
                return HttpResponse('修改成功')


class ShopView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        user = request.user
        if user.group.code==300:
            shop = user.shop_set.all()[0]
            type = request.GET.get('type')
            if type == 'promotion':
                return HttpResponse(json.dumps(list(shop.promotion_set.all().values())))
            return HttpResponseBadRequest('参数错误')
        elif user.group.code==100:
            shops = Shop.objects.all()
            shopArr = []
            for item in shops:
                itemDict = model_to_dict(item)
                itemDict['promotion'] = list(item.promotion_set.all().values())
                shopArr.append(itemDict)
            return HttpResponse(json.dumps(shopArr))


    @method_decorator(loginCheck)
    def put(self, request):
        user_id = request.bodyJson.get('id')
        value = request.bodyJson.get('value')
        type = request.bodyJson.get('type')
        user = request.user
        shop = user.shop_set.all()[0]
        response = HttpResponse()
        response.status_code = 200
        if not all([value, type]):
            response.status_code = 400
            response.content = "参数错误"
        try:
            if type == 'autoAccept':
                value = True if value == 1 else False
                shop.autoAccept = value
            elif type == 'desc':
                shop.desc = value
            elif type == 'name':
                shop.name = value
            elif type == 'thumb':
                shop.thumb = value
            elif type == 'promotion':
                deleteList = request.bodyJson.get('deleteList')
                addArr = []
                updateArr = []
                for item in value:
                    if item.get('id') == None:
                        addArr.append(
                            Promotion(full=item['full'], min=item['min'], shop=shop))
                    else:
                        updateArr.append(Promotion.objects.get(id=item.get('id')))
                Promotion.objects.bulk_create(addArr)
                if len(updateArr) > 0:
                    Promotion.objects.bulk_update(updateArr, ['full', 'min'])
                if len(deleteList)>0:
                    Promotion.objects.filter(id__in=deleteList).delete()
            else:
                response.status_code = 400
                response.content = "参数错误"
                return response
            shop.save()
        except Exception as e:
            response.status_code = 400
            response.content = "参数错误"
            return response
        return HttpResponse('编辑成功')
