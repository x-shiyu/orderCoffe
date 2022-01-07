from django.db.models.aggregates import Sum
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import View
import json
from apps.Goods.models import Goods
from apps.Order.models import OrderGoods
from apps.Order.views import Order
from decorator.auth import loginCheck
import datetime

class ChartsView(View):
    @method_decorator(loginCheck)
    def get(self, request):
      type = request.GET.get('type')
      user = request.user
      # 过去的6个月的每月的销量
      if type=='month':
        data = self.getMonthList(user.shop_set)
        return HttpResponse(json.dumps(data))
      elif type =='goods':
        data = self.getGoodsList(user.shop_set)
        return HttpResponse(json.dumps(data))

    def getGoodsList(self,shops):
      cDate = datetime.datetime.now()
      dataArr = []
      for shop in shops.all():
          year = cDate.year if cDate.month>1 else cDate.year-1
          month = cDate.month if cDate.month>1 else 12
          orders = Order.objects.filter(shop = shop,create_time__gt=datetime.date(year,month,cDate.day)).order_by('create_time')
          # for order in orders:
          order_goods = OrderGoods.objects.filter(order__in=orders).values('goods').annotate(goods_sum=Sum('buy_num'))
          for item in order_goods:
            goods = Goods.objects.get(id=item['goods'])
            dataArr.append({
              "label":goods.name,
              "value":item['goods_sum']
            })
      return dataArr


    def getMonthList(self,shops):
      cDate = datetime.datetime.now()
      dataArr = []
      dataMap = {}
      for shop in shops.all():
          orders = Order.objects.filter(shop = shop,create_time__gt=datetime.date(cDate.year-1,cDate.month,cDate.day)).order_by('create_time')
          for order in orders:
            order_goods = OrderGoods.objects.filter(order=order).aggregate(Sum('buy_num'))
            label = str(order.create_time.year)+'-'+str(order.create_time.month)
            if dataMap.get(label)!=None:
              dataMap[label] = dataMap[label]+order_goods.get('buy_num__sum')
            else:
               dataMap[label] = order_goods.get('buy_num__sum')
      for key in dataMap:
        dataArr.append({
          "label":key,
          "value":dataMap[key]
        })
      return dataArr