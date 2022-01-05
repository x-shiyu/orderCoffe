import json
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from UserInfo.models import Shop
from apps.Goods.models import Category, Goods
from utils.JsonParser import formatJson
from decorator.auth import loginCheck
from apps.File.models import Attachment
# Create your views here.
from django.forms.models import model_to_dict


class CateView(View):
    @method_decorator(loginCheck)
    def get(self, request):
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


class GoodsView(View):
    @method_decorator(loginCheck)
    def get(self, request):
        cateId = request.GET['id']
        keywords = request.GET['keywords'] or ''
        if cateId != None:
            try:
                goods = Goods.objects.filter(category_id=cateId,name__icontains=keywords)
            except Goods.DoesNotExist:
                goods = []
            return HttpResponse(json.dumps(list(goods.values())))
        else:
            response = HttpResponse('参数错误')
            response.status_code = 400
            return response

    @method_decorator(loginCheck)
    def put(self, request):
        discount = request.bodyJson['discount']
        name = request.bodyJson['name']
        price = request.bodyJson['price']
        thumb = request.bodyJson['thumb']
        desc = request.bodyJson['description']
        cate_id = request.bodyJson['cate_id']
        goods_id = request.bodyJson['id']
        response = HttpResponse()
        response.status_code = 200
        if not all([name, price, thumb, desc, goods_id]):
            response.status_code = 400
            response.content = "缺少参数"
            return response
        try:
            cate = Category.objects.get(Q(id=cate_id))
            thumb = Attachment.objects.get(Q(id=thumb))
            Goods.objects.filter(id=goods_id).update(name=name, description=desc, price=price,
                                          category=cate, thumb=thumb, discount=discount)
        except Exception:
            print('更新失败-->', Exception)
            response.status_code = 400
            response.content = '参数错误'
            return response
        return response

    @method_decorator(loginCheck)
    def post(self, request):
        discount = request.bodyJson['discount']
        name = request.bodyJson['name']
        price = request.bodyJson['price']
        thumb = request.bodyJson['thumb']
        desc = request.bodyJson['description']
        cate_id = request.bodyJson['cate_id']
        response = HttpResponse()
        response.status_code = 200

        if not all([name, price, thumb, desc]):
            response.status_code = 400
            response.content = "缺少参数"
            return response
        try:
            cate = Category.objects.get(Q(id=cate_id))
            thumb = Attachment.objects.get(Q(id=thumb))
            goods = Goods.objects.create(
                name=name, description=desc, price=price, category=cate, thumb=thumb, discount=discount)
        except Exception:
            print('创建商品失败-->', Exception)
            response.status_code = 400
            response.content = '参数错误'
            return response
        response.content = json.dumps({
            "id": goods.pk
        })
        return response




class ShopGoodsView(View):
    @method_decorator(loginCheck)
    def get(self,request):
        shop_id = request.GET.get('id')
        goods = Shop.objects.get(id=shop_id).goods_set.all()
        goodsArr = []
        for item in goods:
          itemDict = model_to_dict(item)
          itemDict['category_name'] = item.category.category_name
          goodsArr.append(itemDict)
        return HttpResponse(json.dumps(goodsArr))
