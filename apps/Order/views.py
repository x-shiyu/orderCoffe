from django.shortcuts import render
import json
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.generic import View
from django.utils.decorators import method_decorator
from UserInfo.models import Promotion, Shop
from apps.Goods.models import Category, Goods
from apps.Order.models import Order
from utils.JsonParser import formatJson
from decorator.auth import loginCheck
from apps.File.models import Attachment
# Create your views here.

class OrderView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        user = request.user
        # 商户的订单列表
        if user.group_id ==1:
          order_status = request.GET.get('status')
          shop = user.shop_set.all()[0]
          if order_status !=None:
            orders = shop.order_set.filter(status=order_status)
          else:
            orders = shop.order_set.all()
          return HttpResponse(json.dumps(list(orders)))
        else:
          return HttpResponse(json.dumps([]))

    @method_decorator(loginCheck)
    def post(self, request):
        user = request.user
        if user.group_id==2:
          shop_id = request.bodyJson['shop_id']
          goods = request.bodyJson['goods']
          real_pay = request.bodyJson['real_pay']
          promotion_id = request.bodyJson['promotion_id']
          response = HttpResponse()
          response.status_code = 200
          if not all([shop_id, goods,real_pay,promotion_id]):
            response.status_code = 400
            response.content = "缺少参数"
            return response
          try:
            shop = Shop.objects.get(id=shop_id)
            goods = Goods.objects.filter(id__in=goods)
            promotion = Promotion.objects.get(id=promotion_id)
            abstract_pay = float(user.abstract_money)
            Order.objects.create(customer=user,shop=shop,goods=goods,real_pay=real_pay,status=1,abstract_pay=abstract_pay,promotion=promotion)
          except Shop.DoesNotExist:
            return HttpResponseBadRequest('没有此商家')
          except Goods.DoesNotExist:
            return HttpResponseBadRequest('没有此商品')
          except Exception as e:
            return HttpResponseServerError('创建订单失败')
        elif user.group_id==1:
          order_id = request.bodyJson['order_id']
          return HttpResponseBadRequest('用户错误！')
     