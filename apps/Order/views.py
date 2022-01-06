from django.forms.models import model_to_dict
from django.shortcuts import render
import json
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.generic import View
from django.utils.decorators import method_decorator
from UserInfo.models import Promotion, Shop
from apps.Goods.models import Category, Goods
from apps.Order.models import Order, OrderGoods
from utils.JsonParser import formatJson
from decorator.auth import loginCheck


class OrderView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        user = request.user
        # 商户的订单列表
        if user.group.code == 300:
            order_status = request.GET.get('status')
            resArr = []
            shop = user.shop_set.all()[0]
            if order_status != None:
                orders = shop.order_set.filter(status=order_status)
            else:
                orders = shop.order_set.all()
            for item in orders:
                matchGoods = OrderGoods.objects.filter(order=item)
                goodsArr = []

                for g in matchGoods:
                    goodsArr.append({
                        "thumb": g.goods.thumb.id,
                        "name": g.goods.name
                    })

                resArr.append({
                    "createTime": item.create_time.timestamp(),
                    "name": item.shop.name,
                    "goodsList": goodsArr,
                    "id": item.id,
                    "thumb": item.shop.thumb.id,
                    "totalPrice": item.real_pay,
                    "status": item.status,
                    "discount": list(item.shop.promotion_set.all().values())
                })
            return HttpResponse(json.dumps(resArr))
        elif user.group.code == 100:
            resArr = []
            orders = Order.objects.filter(
                customer_id=user.id).order_by('create_time').reverse()
            for item in orders:
                matchGoods = OrderGoods.objects.filter(order=item)
                goodsArr = []

                for g in matchGoods:
                    goodsArr.append({
                        "thumb": g.goods.thumb.id,
                        "name": g.goods.name
                    })

                resArr.append({
                    "createTime": item.create_time.timestamp(),
                    "name": item.shop.name,
                    "goodsList": goodsArr,
                    "id": item.id,
                    "thumb": item.shop.thumb.id,
                    "totalPrice": item.real_pay,
                    "status": item.status,
                    "discount": list(item.shop.promotion_set.all().values())
                })
            return HttpResponse(json.dumps(resArr))

    @method_decorator(loginCheck)
    def post(self, request):
        user = request.user
        if user.group.code == 100:
            shop_id = request.bodyJson.get('shop_id')
            goods = request.bodyJson.get('goods')
            real_pay = request.bodyJson.get('real_pay')
            promotion_id = request.bodyJson.get('promotion_id')
            totalPay = request.bodyJson.get('totalPay')
            abstract_money = float(user.abstract_money)/100
            response = HttpResponse()
            response.status_code = 200
            if not all([shop_id, goods, real_pay]):
                response.status_code = 400
                response.content = "缺少参数"
                return response
            try:
                shop = Shop.objects.get(id=shop_id)
                totalCount = 0
                order_goods_arr = []

                promotion = Promotion.objects.get(
                    id=promotion_id) if promotion_id != None else None
                abstract_pay = abstract_money if float(
                    totalPay) - abstract_money > 0 else (abstract_money-float(totalPay))
                status = 2 if shop.autoAccept else 1
                order_new = Order.objects.create(
                    customer=user, shop=shop, real_pay=real_pay, status=status, abstract_pay=abstract_pay, promotion=promotion)

                for key in goods:
                    goodsIn = Goods.objects.get(id=key)
                    order_goods_arr.append(OrderGoods(
                        order=order_new, goods=goodsIn, buy_num=goods[key]))
                    totalCount += goods[key]
                    goodsIn.month_sell = goodsIn.month_sell+goods[key]
                    goodsIn.save()

                shop.monthSell = shop.monthSell+totalCount
                shop.save()
                OrderGoods.objects.bulk_create(order_goods_arr)
                user.abstract_money = user.abstract_money - \
                    abstract_pay*100+int((totalPay / 100)*10)
                user.save()
                return HttpResponse('下单成功！')
            except Shop.DoesNotExist:
                return HttpResponseBadRequest('没有此商家')
            except Goods.DoesNotExist:
                return HttpResponseBadRequest('没有此商品')
            except Exception as e:
                return HttpResponseServerError('创建订单失败')
        else:
          return HttpResponseBadRequest('请求失败')

    @method_decorator(loginCheck)
    def put(self, request):
      user = request.user
      if user.group.code == 300:
        order_id = request.bodyJson.get('order_id')
        accept = request.bodyJson.get('accept')
        if not all([order_id, accept]):
          return HttpResponseBadRequest('缺少参数')
        order = Order.objects.get(id=order_id)
        if accept==1:
          order.status = 2
        elif accept==2:
          order.status = 4
        else:
          return HttpResponseBadRequest('参数错误！')
        order.save()
        return HttpResponse('操作成功！')
        
      elif user.group.code == 100:
        order_id = request.bodyJson.get('order_id')
        if not all([order_id]):
          return HttpResponseBadRequest('缺少参数')
        order = Order.objects.get(id=order_id)
        order.status = 3
        order.save()
        return HttpResponse('操作成功！')