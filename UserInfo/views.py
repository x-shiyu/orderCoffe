from django.http.response import HttpResponse
from UserInfo.models import User, Group, Shop

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.generic import View
from django.conf import settings
from File.models import Attachment
import re

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
        # 进行数据校验
        if not all([password, email,code]):
            # 数据不完整
            response.status_code = 400
            response.content = '缺少用户名或密码'
            return response
        if code != 100 and code !=300:
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
            group_name = "客户" if code==100 else 300
            group = Group.objects.create(code=code,name=group_name)
        except Attachment.DoesNotExist:
            image = Attachment.objects.create(file_name="default",file_path='default.jpg')
        user.group = group
        user.thumb = image
        user.save()
        response.status_code = 200
        response.content = 'ok'
        return response


'''
class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取要激活的哟用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活的用户id
            user_id = info['confirm']

            # 根据id获取用户的信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登陆页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 激活连接已经
            return HttpResponse('激活连接已过期')

'''


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
        user = authenticate(request,email=email, password=password)
        if user is not None:
            # 用户名已激活
            login(request, user)
            # 跳转到首页
            return response
        else:
            response.status_code = 400
            response.content = '用户名或密码错误'
            return response


'''

# user logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """退出登录"""
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    def get(self, request):
        """显示"""
        # page='user'
        # 如果用户未登录->AnonymousUser类的一个实例
        # 如果用户登录->User类的一个实例
        # request.user.is_authenticated()
        # 文档地址：https://yiyibooks.cn/xx/django_182/topics/auth/default.html#user-objects
        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的历史记录
        # from redis import StrictRedis
        # sr = StrictRedis(host="127.0.0.1", port="6379", db=9)
        con = get_redis_connection('default')

        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)

        # 从数据库中查询用户浏览的商品的具体信息
        #goods_li = GoodsSKU.objects.filter(id__in=sku_ids)

        # 第一种方式
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)

        # 第二种方式：对应id一个一个的从数据库拿
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}

        return render(request, 'user_center_info.html', context)

# /user/order


class UserOrderView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    def get(self, request, page):
        """显示"""
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 便利获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 便利order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount，保存订单商品的小计
                order_sku.amount = amount
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        print(order_page)
        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'}

        return render(request, 'user_center_order.html', context)

# /uesr/address


class AddressView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    def get(self, request):
        """显示"""
        # page='address'
        # 获取登录用户的对应的User对象
        user = request.user

        # 获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收获地址
        #     address = None
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        """地址的添加"""
        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验数据
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收获地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户的对应的User对象
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收获地址
        #     address =None
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               phone=phone,
                               zip_code=zip_code,
                               is_default=is_default)

        # 返回应答,刷新地址页面 get请求
        return redirect(reverse('user:address'))
'''
