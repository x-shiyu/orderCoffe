import json
from django.http import response
from django.http.response import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.Goods.models import Category
from utils.JsonParser import formatJson
# Create your views here.

class CateView(View):
  @method_decorator(login_required)
  def get(self,request):
    #  id: Date.now(),
    #  name: request.body.cate,
    #  desc: request.body.desc,
    allCate = request.user.shop_set.all()[0].category_set.all()
    return HttpResponse(formatJson(allCate))



  @method_decorator(login_required)
  def post(self,request):
    cate = request.bodyJson['cate']
    desc = request.bodyJson['desc']
    response = HttpResponse()
    response.status_code = 200

    if not all([cate, desc]):
      response.status_code = 400
      response.content="缺少参数"
      return response
    try:
      cateIn = Category.objects.create(category_name=cate,description = desc,shop=request.user.shop_set.all()[0])
    except Exception:
      print('创建类别错误-->',Exception)
      response.status_code = 500
      return response
    return HttpResponse(json.dumps({
      "name":cate,
      "desc":desc,
      "id":cateIn.id
    }))



class GoodsView(View):
  @method_decorator(login_required)
  def get(self,request):
    #  id: Date.now(),
    #  name: request.body.cate,
    #  desc: request.body.desc,
    allCate = request.user.shop_set.all()[0].category_set.all()
    return HttpResponse(formatJson(allCate))



  @method_decorator(login_required)
  def post(self,request):
    cate = request.bodyJson['cate']
    desc = request.bodyJson['desc']
    response = HttpResponse()
    response.status_code = 200

    if not all([cate, desc]):
      response.status_code = 400
      response.content="缺少参数"
      return response
    try:
      cateIn = Category.objects.create(category_name=cate,description = desc,shop=request.user.shop_set.all()[0])
    except Exception:
      print('创建类别错误-->',Exception)
      response.status_code = 500
      return response
    return HttpResponse(json.dumps({
      "name":cate,
      "desc":desc,
      "id":cateIn.id
    }))

