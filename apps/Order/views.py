from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from apps.Goods.models import Category, Goods
from apps.Order.models import Order
from utils.JsonParser import formatJson
from decorator.auth import loginCheck
from apps.File.models import Attachment
# Create your views here.

class OrderView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        user_type = request.user.group_id
        if user_type ==1:
          shop_id = request.user.shop_set.all()[0].id
          order_list = Order.objects.filter(shop_id=shop_id)
        allCate = request.user.shop_set.all()[0].category_set.all()
        return HttpResponse(formatJson(allCate))

    @method_decorator(loginCheck)
    def post(self, request):
        cate = request.bodyJson['cate']
        desc = request.bodyJson['desc']
        response = HttpResponse()
        response.status_code = 200

        if not all([cate, desc]):
            response.status_code = 400
            response.content = "缺少参数"
            return response
        try:
            cateIn = Category.objects.create(
                category_name=cate, description=desc, shop=request.user.shop_set.all()[0])
        except Exception:
            print('创建类别错误-->', Exception)
            response.status_code = 500
            return response
        return HttpResponse(json.dumps({
            "name": cate,
            "desc": desc,
            "id": cateIn.id
        }))

